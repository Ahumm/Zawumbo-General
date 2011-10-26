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

void checkBackupDirectory(){
    int rc = 0;
    /*char* cwd;
    struct stat d_stat;
    DIR* dir;
    struct dirent* de;
    
    getcwd(cwd);
    
    // Open the current directory
    dir = opendir(".");
    if(!dir){
        perror("opendir: %s", cwd);
        return "";
    }
    
    while(de = readdir(dir)) {
        // Skip if not a directory
        if(stat(de->d_name, &d_stat) == -1){
            continue;
        }
        // If directory
        if(S_ISDIR(d_stat.st_mode)){
            // Check for a match, return if found
            if (de->d_name && strstr(de->d_name, ".mybackup"){
                return;
            }
        }
    }
    */
    // Directory not found, make it
    rc = mkdir(".mybackup",0777);
    if (rc < 0){
        if(errno != EEXIST){
            perror("mkdir:");
        }
    }
    //free(cwd);
}

int fileExists(char* name){
    struct stat d_stat;
    int rc = 0;
    
    rc = stat(name,&d_stat);
    if (rc == 0){
        return 1;
    }
    return 0;
}

// BACKUP LOGIC

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
    
    sprintf(dest,"./.mybackup/%s.bak",filename);

    sprintf(src,"./%s",filename);

    // Open original file
    if((from = open(src,O_RDONLY))<0){
        perror("Open Src: ");
        return NULL;
    }
    
    exists = fileExists(dest);
    if( exists ){
        if(stat(src,&s_stat) < 0){
	    perror("src stat: ");
	    return NULL;
	}
	if(stat(dest,&d_stat) < 0){
	    perror("dest stat: ");
            return NULL;
	}

	if(s_stat.st_mtime < d_stat.st_mtime){
	    printf("[THREAD %u] Backup copy of %s alrady up-to-date\n",(unsigned int)pthread_self(),filename);
	    return 0;
	}
        printf("[THREAD %u] WARNING: %s.bak exists (overwriting!)\n", (unsigned int)pthread_self(),filename);
    }
    
    if((to = open(dest,O_RDWR|O_TRUNC|O_CREAT,(S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH)))<0){
        perror("Open dest: ");
        return NULL;
    }
    
    while (1){
        bytesread = read(from,readdata,READ_BYTES);
        *totalBytesRead += (int)bytesread;
	write(to,readdata,bytesread);
	if(bytesread < READ_BYTES){
	    break;
	}
    }
    
    if(close(from)<0){
        perror("src close: ");
        return NULL;
    }
    if(close(to)<0){
        perror("dest close: ");
        return NULL;
    }
    
    printf("[THREAD %u] Copied %d bytes from %s to %s.bak\n", (unsigned int)pthread_self(),(*totalBytesRead),filename,filename);
    
    return totalBytesRead;
}

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
	    if(!strstr(arg0,de->d_name)){
                numfiles++;
	    }
        }
    }
    closedir(dir);
    
    // Allocate thread space
    threads = (pthread_t *)malloc(numfiles*sizeof(*threads));
    
    // Open the current directory for execute
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
	  if(!strstr(arg0,de->d_name)){
	      if(pthread_create(&threads[curthread],NULL,backup,&de->d_name)){
                    perror("pthread_create: ");
              }  
	      curthread++;
	    }
        }
    }
    closedir(dir);

    for(i = 0; i < curthread; i++){
        pthread_join(threads[i],&t_bytes);
	if(t_bytes){
	    bytesbak = bytesbak + *(int*)t_bytes;
        }
	else{
	    numfiles--;
	}
    }
    
    printf("Successfully backed up %d files (%d bytes)\n",numfiles,bytesbak);
}

// RESTORE LOGIC

void *restore(void* arg){
    char* filename = (char*)arg;
    size_t from,to;
    char dest[MAX_PATH];
    char dest_t[MAX_PATH];
    char src[MAX_PATH];
    char readdata[READ_BYTES];
    ssize_t bytesread;
    int * totalBytesRead = (int*)malloc(sizeof(int));
    int exists = 0;

    *totalBytesRead = 0;

    printf("[THREAD %u] Restoring %s.bak...\n", (unsigned int)pthread_self(),filename);
    
    sprintf(src,"./.mybackup/%s",filename);

    strncpy(dest_t,filename,strlen(filename)-4);
    dest_t[strlen(filename)-4] = '\0';
    sprintf(dest,"./%s",dest_t);

    // Open original file
    if((from = open(src,O_RDONLY))<0){
        perror("Open Src: ");
        return NULL;
    }
    
    exists = fileExists(dest);
    if( exists ){
      //printf("[THREAD %u] WARNING: %s.bak exists (overwriting!)\n", (unsigned int)pthread_self(),filename);
    }
    
    if((to = open(dest,O_RDWR|O_TRUNC|O_CREAT,(S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH)))<0){
        perror("Open dest: ");
        return NULL;
    }
    
    while (1){
        bytesread = read(from,readdata,READ_BYTES);
        *totalBytesRead += (int)bytesread;
	write(to,readdata,bytesread);
	if(bytesread < READ_BYTES){
	    break;
	}
    }
    
    if(close(from)<0){
        perror("src close: ");
        return NULL;
    }
    if(close(to)<0){
        perror("dest close: ");
        return NULL;
    }
    
    printf("[THREAD %u] Copied %d bytes from %s.bak to %s\n", (unsigned int)pthread_self(),(*totalBytesRead),dest_t,dest_t);
    
    return totalBytesRead;
}

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
    
    getcwd(cwd,80);
    
    // Open the current directory for count
    dir = opendir("./.mybackup");
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
            numfiles++;
        }
    }
    closedir(dir);
    
    // Allocate thread space
    threads = (pthread_t *)malloc(numfiles*sizeof(*threads));
    
    // Open the current directory for execute
    dir = opendir("./.mybackup");
    if(!dir){
        fprintf(stderr,"opendir: %s", cwd);
        return;
    }
    while((de = readdir(dir))) {
        sprintf(actualPath,"./.mybackup/%s",de->d_name);
        // Get stat
        if(stat(actualPath, &d_stat) == -1){
            continue;
        }
        // If regular file
        if(S_ISREG(d_stat.st_mode)){
	  if(!strstr(arg0,de->d_name)){
	      if(pthread_create(&threads[curthread],NULL,restore,&de->d_name)){
                    perror("pthread_create: ");
                }  
                curthread++;
	    }
        }
    }
    closedir(dir);
    
    for(i = 0; i < curthread; i++){
        pthread_join(threads[i],&t_bytes);
	if(t_bytes){
	  bytesbak = bytesbak + *(int*)t_bytes;
        }
    }
    
    printf("Successfully backed up %d files (%d bytes)\n",curthread,bytesbak);
}


int main(int argc, char *argv[]){
    checkBackupDirectory();
    if(argc == 1){
        backupFiles(argv[0]);
    }
    else if(argc == 2 && !strcmp(argv[1],"-r")){
      restoreFiles(argv[0]);
    }
    else{
      fprintf(stderr,"USAGE: %s [-r]\n",argv[0]);
      exit(1);
    }
    return 0;
}
