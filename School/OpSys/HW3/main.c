#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>

#include <errno.h>
extern int errno;

#define MAX_THREADS 1000
#define MAX_PATH 80

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
        if(errno != EEXISTS){
          perror("mkdir:");
        }
    }
    //free(cwd);
}

int fileExists(char* filename){
    struct stat d_stat;
    int rc = 0;
    
    rc = stst(filename,&d_stat);
    if (re == 0){
        return 1;
    }
    return 0;
}

int backup(char* filename){
    FILE *from,*to;
    char ch;
    char dest[MAX_PATH] = '\0';
    int charscopied = 0;
    int exists = 0;

    printf("[THREAD %d] Backing Up %s...\n", (unsignedint)pthread_self(),filename);
    
    strncat(dest,".mybackup",sizeof(dest)-strlen(dest)-1);
    strncat(dest,filename,sizeof(dest)-strlen(dest)-1);
    strncat(dest,".bak",sizeof(dest)-strlen(dest)-1);
    
    // Open original file
    if((from = fopen(filename,"r"))==NULL){
        perror("Open Src: ");
        return -1;
    }
    
    exists = fileExists(dest);
    if( exists ){
        printf("[THREAD %d] WARNING: %s.bak exists(overwriting!)\n", (unsignedint)pthread_self(),filename);
    }
    
    if((to = fopen(dest,"w"))==NULL){
        perror("Open dest: ");
        return -1;
    }
    
    while (!feof(from)){
        ch = fgetc(from);
        if ferror(from)){
            fprintf(stderr,"src read error\n");
            return -1;
        }
        if !feof(from){
            fputc(ch,to);
        }
        if(ferror(to)){
            fprintf(stderr,"dest write error\n");
            return -1;
        }
        charscopied++;
    }
    
    if(fclose(from)==EOF){
        fprintf(stderr,"src close error\n");
        return -1;
    }
    if(fclose(to)==EOF){
        fprintf(stderr,"dest close error\n");
        return -1;
    }
    
    printf("[THREAD %d] Copied %d bytes from %s to %s.bak\n", (unsignedint)pthread_self(),charscopied,filename,filename);
    
    return charscopied;
}

void backupFiles(){
    struct stat d_stat;
    DIR* dir;
    struct dirent* de;
    pthread_t* threads;
    int numthreads = 0;
    int numfiles = 0;
    int i = 0;
    int curthread = 0;
    int bytesbak = 0;
    int** t_bytes;
    
        getcwd(cwd);
    
    // Open the current directory for count
    dir = opendir(".");
    if(!dir){
        perror("opendir: %s", cwd);
        return "";
    }
    while(de = readdir(dir)) {
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
    dir = opendir(".");
    if(!dir){
        perror("opendir: %s", cwd);
        return "";
    }
    while(de = readdir(dir)) {
        // Get stat
        if(stat(de->d_name, &d_stat) == -1){
            continue;
        }
        // If regular file
        if(S_ISREG(d_stat.st_mode)){
            if(!pthread_create(&threads[curthread],NULL,backup,de->d_name)){
                perror("pthread_create: ");
            }
            curthread++;
        }
    }
    closedir(dir);
    
    for(i = 0; i < curthread; i++){
        pthread_join(threads[i],t_bytes);
        bytesbak = bytesbak + t_bytes;
    }
    
    printf("Successfully backed up %d files (%d bytes)\n",curthread,bytesbak);
}

int main(int argc, char *argv[]){
    checkBackupDirectory();
    if(argc == 1){
        backupFiles();
    }
    else if(argc == 2){
    }
}