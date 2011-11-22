/*
 * Tate Larsen
 * Operating Systems
 * Homework 3
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <pthread.h>
#include <fcntl.h>

#include <errno.h>
extern int errno;

#define MAX_THREADS 1000
#define MAX_PATH 80
#define READ_BYTES 256


// Create the backup directory if needed
void checkBackupDirectory(){
    int rc = 0;
    // Try to create the directory, 
    //   will fail if it exists but we don't care so ignore that error number
    rc = mkdir(".mybackup",0777);
    if (rc < 0){
        if(errno != EEXIST){
            perror("mkdir:");
        }
    }
}

// Check if a file exists
int fileExists(char* name){
    struct stat d_stat;
    int rc = 0;
    
    rc = stat(name,&d_stat);
    if (rc == 0){
        // File exists
        return 1;
    }
    // File does not exist
    return 0;
}

// BACKUP FUNCTIONS

/*
 *
 * Backup a file to the ./.mybackup directory
 * recieves: name of the file to be backed up
 * Returns:  number fo bytes backed up
 *
 */
void *backup(void* arg){
    char* filename = (char*)arg;
    size_t from,to;
    char dest[MAX_PATH];
    char src[MAX_PATH];
    char readdata[READ_BYTES];
    ssize_t bytesread;
    int * totalBytesRead = (int*)malloc(sizeof(int));
    int exists = 0;
    struct stat d_stat;
    struct stat s_stat;

    *totalBytesRead = 0;

    printf("[THREAD %u] Backing Up %s...\n", (unsigned int)pthread_self(),filename);
    
    // Set source and destination paths
    sprintf(dest,"./.mybackup/%s.bak",filename);

    sprintf(src,"./%s",filename);

    // Open original file
    if((from = open(src,O_RDONLY))<0){
        perror("Open Src: ");
        return NULL;
    }
    
    // Check if a backup already exists
    exists = fileExists(dest);
    if( exists ){
        // Get info about original and existing backup
        if(stat(src,&s_stat) < 0){
	    perror("src stat: ");
	    return NULL;
	}
	if(stat(dest,&d_stat) < 0){
	    perror("dest stat: ");
            return NULL;
	}

	// Check to see if the original file has been modified since 
	//   the existing backup was created
	if(s_stat.st_mtime < d_stat.st_mtime){
	    // It has not, do not back up
	    printf("[THREAD %u] Backup copy of %s alrady up-to-date\n",(unsigned int)pthread_self(),filename);
	    return 0;
	}
	// It has, backup
        printf("[THREAD %u] WARNING: %s.bak exists (overwriting!)\n", (unsigned int)pthread_self(),filename);
    }
    
    // Open and clean or create destination file
    if((to = open(dest,O_RDWR|O_TRUNC|O_CREAT,(S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH)))<0){
        perror("Open dest: ");
        return NULL;
    }
    
    // Backup
    while (1){
        // Read from orginal
        bytesread = read(from,readdata,READ_BYTES);

	// Keep track of bytes read
        *totalBytesRead += (int)bytesread;

	// Write to backup
	write(to,readdata,bytesread);

	// Reached end of original so break
	if(bytesread < READ_BYTES){
	    break;
	}
    }
    
    // Close the original
    if(close(from)<0){
        perror("src close: ");
        return NULL;
    }

    // Close the backup
    if(close(to)<0){
        perror("dest close: ");
        return NULL;
    }
    
    // Print some information
    printf("[THREAD %u] Copied %d bytes from %s to %s.bak\n", (unsigned int)pthread_self(),(*totalBytesRead),filename,filename);
    
    // Return bytes backed up
    return totalBytesRead;
}

/*
 *
 * Backs up files in current directory
 * recieves: name of this program
 *
 */
void backupFiles(char* arg0){
    struct stat d_stat;
    DIR* dir;
    struct dirent* de;
    pthread_t* threads;
    int numfiles = 0;
    int i = 0;
    int curthread = 0;
    int bytesbak = 0;
    void* t_bytes = 0;
    char cwd[80];
    
    cwd[0] = '\0';
    
    // Get the path to the current directory
    getcwd(cwd,80);
    
    // Open the current directory for count
    dir = opendir(".");
    if(!dir){
        fprintf(stderr, "opendir: %s", cwd);
        return;
    }
    while((de = readdir(dir))) {
        // Get stat
        if(stat(de->d_name, &d_stat) == -1){
            continue;
        }
        // If regular file
        if(S_ISREG(d_stat.st_mode)){
	    // Count files
	    if(!strstr(arg0,de->d_name)){
                numfiles++;
	    }
        }
    }
    // Close the directory
    closedir(dir);
    
    // Allocate thread space
    threads = (pthread_t *)malloc(numfiles*sizeof(*threads));
    
    // Open the current directory for backup
    dir = opendir(".");
    if(!dir){
        fprintf(stderr,"opendir: %s", cwd);
        return;
    }
    while((de = readdir(dir))) {
        // Get stat
        if(stat(de->d_name, &d_stat) == -1){
            continue;
        }
        // If regular file
        if(S_ISREG(d_stat.st_mode)){
	  // Back it up if it isn't this program
	  if(!strstr(arg0,de->d_name)){
	      if(pthread_create(&threads[curthread],NULL,backup,&de->d_name)){
                    perror("pthread_create: ");
              }
	      curthread++;
	    }
        }
    }
    // Close the directory
    closedir(dir);

    // Join the threads, keep track of bytes and files backed up
    for(i = 0; i < curthread; i++){
        pthread_join(threads[i],&t_bytes);
	if(t_bytes){
	    bytesbak = bytesbak + *(int*)t_bytes;
        }
	else{
	    numfiles--;
	}
    }
    
    // Print some information
    printf("Successfully backed up %d files (%d bytes)\n",numfiles,bytesbak);
}



// RESTORE FUNCTIONS

/*
 *
 * restore a file from the ./.mybackup directory
 * recieves: name of the file to be backed up
 * Returns:  number fo bytes backed up
 *
 */
void *restore(void* arg){
    char* filename = (char*)arg;
    size_t from,to;
    char dest[MAX_PATH];
    char dest_t[MAX_PATH];
    char src[MAX_PATH];
    char readdata[READ_BYTES];
    ssize_t bytesread;
    int * totalBytesRead = (int*)malloc(sizeof(int));

    *totalBytesRead = 0;

    printf("[THREAD %u] Restoring %s.bak...\n", (unsigned int)pthread_self(),filename);
    
    // Determine source and destination paths
    sprintf(src,"./.mybackup/%s",filename);

    strncpy(dest_t,filename,strlen(filename)-4);
    dest_t[strlen(filename)-4] = '\0';
    sprintf(dest,"./%s",dest_t);

    // Open backup file
    if((from = open(src,O_RDONLY))<0){
        perror("Open Src: ");
        return NULL;
    }
    
    // Open/Create restore file
    if((to = open(dest,O_RDWR|O_TRUNC|O_CREAT,(S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH)))<0){
        perror("Open dest: ");
        return NULL;
    }
    
    // Restore the file
    while (1){
        // Read from backup
        bytesread = read(from,readdata,READ_BYTES);
        
	// Keep track of bytes restored
	*totalBytesRead += (int)bytesread;

	// Write to restoration
	write(to,readdata,bytesread);
	
	// End of backup reached
	if(bytesread < READ_BYTES){
	    break;
	}
    }
    
    // Close backup
    if(close(from)<0){
        perror("src close: ");
        return NULL;
    }

    // Close restoration
    if(close(to)<0){
        perror("dest close: ");
        return NULL;
    }

    // Print some info
    printf("[THREAD %u] Copied %d bytes from %s.bak to %s\n", (unsigned int)pthread_self(),(*totalBytesRead),dest_t,dest_t);
    
    // Return bytes restored
    return totalBytesRead;
}

/*
 *
 * Backs up files in current directory
 * recieves: name of this program
 *
 */
void restoreFiles(char* arg0){
    struct stat d_stat;
    DIR* dir;
    struct dirent* de;
    pthread_t* threads;
    int numfiles = 0;
    int i = 0;
    int curthread = 0;
    int bytesbak = 0;
    void* t_bytes = 0;
    char cwd[80];
    char actualPath[MAX_PATH];
    
    cwd[0] = '\0';
    actualPath[0] = '\0';
    

    // Get absolute path to current directory
    getcwd(cwd,80);
    
    // Open the backup directory for count
    dir = opendir("./.mybackup");
    if(!dir){
        fprintf(stderr, "opendir: %s", cwd);
        return;
    }
    // Count files to be restored
    while((de = readdir(dir))) {
        // Get stat
        if(stat(de->d_name, &d_stat) == -1){
            continue;
        }
        // If regular file
        if(S_ISREG(d_stat.st_mode)){
            numfiles++;
        }
    }
    // Close the directory
    closedir(dir);

    // Nothing to restore, so return
    if(numfiles == 0){
        // Remove the backup directory we created if empty
        if(rmdir("./.mybackup") == 0){
	    printf("[THREAD %u] No files to restore, exiting...\n", (unsigned int)pthread_self());
        }
        return;
    }
    
    // Allocate thread space
    threads = (pthread_t *)malloc(numfiles*sizeof(*threads));
    
    // Open the backup directory for execute
    dir = opendir("./.mybackup");
    if(!dir){
        fprintf(stderr,"opendir: %s", cwd);
        return;
    }
    // Restore files
    while((de = readdir(dir))) {
        // Needed for stat
        sprintf(actualPath,"./.mybackup/%s",de->d_name);
        // Get stat
        if(stat(actualPath, &d_stat) == -1){
            continue;
        }
        // If regular file
        if(S_ISREG(d_stat.st_mode)){
	    // Ignore this program
	    if(!strstr(arg0,de->d_name)){
	        // Create the restore thread
	        if(pthread_create(&threads[curthread],NULL,restore,&de->d_name)){
                    perror("pthread_create: ");
                }  
                curthread++;
            }
        }
    }
    // Chose the directory
    closedir(dir);
    
    // Join the threads
    for(i = 0; i < curthread; i++){
        pthread_join(threads[i],&t_bytes);
	// Count bytes restored
	if(t_bytes){
	  bytesbak = bytesbak + *(int*)t_bytes;
        }
    }
    
    // Print some information
    printf("Successfully backed up %d files (%d bytes)\n",curthread,bytesbak);
}


int main(int argc, char *argv[]){
    // Make the backup directory if it doesn't exist
    checkBackupDirectory();
    // Back up files
    if(argc == 1){
        backupFiles(argv[0]);
    }
    // Restore files
    else if(argc == 2 && !strcmp(argv[1],"-r")){
      restoreFiles(argv[0]);
    }
    // Improper usage
    else{
      fprintf(stderr,"USAGE: %s [-r]\n",argv[0]);
      exit(1);
    }
    return 0;
}
