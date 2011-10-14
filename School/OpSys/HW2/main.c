#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>

int MAX_PATH = 256;

void findcommand(char* cmd);

int main() {
    char* MYPATH = getenv("PATH");
    int found = 0;
    char* cmdpath;
    char base_path[MAX_PATH+1];
    char* token, search = ":";
    char* expcmd;
    
    
    printf("Welcome to myshell.\nMYPATH= %s\n", MYPATH);
    
    while ( 1 ) {
        /* get command from the user */
        char cmd[80];

        printf("--| ");
        scanf( "%[^\n]", cmd );
        getchar();  /* consume the '\n' character */

        printf("Okay, you entered \"%s\"\n", cmd );
        
        if(!strcmp("exit", cmd) || !strcmp("quit", cmd)){
            printf("Exiting...\n");
            return 0;
        }
        
        /* validate the command, find the command in $MYPATH */
        if(!getcwd(base_path, MAX_PATH + 1)){
            perror("getcwd: ");
            continue;
        }
        expcmd = strtok(cmd, " ");
        token = strtok(MYPATH, search);
        while (token != NULL){
            chdir(token);
            cmdpath = findcommand(expcmd);
            if (cmdpath){
                found = 1;
                break;
            }
        }
        
        chdir(cwd);

        if(!found){
            printf("ERROR: command \"%s\" is not recognized."), cmd);
        }
        else{
            /* create a child process to execute the command
            pid = fork();

            if ( pid == 0 ) {
                /* execute command via exec() */

                /* what if the cmd is:   ls -l ==> file.txt */
                /*   use dup2() here for redirection */
                exit( 1 );  /* child should not reach this point */
            }
            else if ( pid > 0 ) {
                wait();   /* unless the user has & at the end of the command */
            }
        }
    }

    return 0;
}

/*
 * Tries to find a command in the current directory
 */
char* findcommand(char* cmd){
    DIR* dir;
    struct dirent* de;
    char cwd[MAX_PATH + 1];
    struct stat d_stat;
    char* found;
    
    // Save current directory (for jump back)
    if(!getcwd(cwd, MAX_PATH + 1)){
        perror("getcwd:");
        return "";
    }
    
    // Open the directory
    dir = opendir(".");
    if(!dir){
        perror("opendir: %s", cwd);
        return "";
    }
    
    //Look through directory and sub-directories for the command
    while(de = readdir(dir)) {
        // Check for a match
        if (de->d_name && strstr(de->d_name, cmd){
            return strcat(cwd/de->d_name);
        }
        // Skip if not a directory
        if(stat(de->d_name, &d_stat) == -1){
            continue;
        }
        // Avoid "." and ".." directories
        if(strcmp(de->d_name, ".") || strcmp(de->d_name, "..")){
            continue;
        }
        // Traverse the sub directory if it is one
        if(S_ISDIR(d_stat.st_mode)){
            // Move into the subdirectory
            if(chdir(de->d_name) == -1){
                perror("chdir: %s", de->d_name);
                continue;
            }
            
            // Look for the command and return the path if found
            found = findcommand(cmd);
            if(found){
                return found;
            }
            
            // Move back up otherwise
            if(chdir("..") == -1){
                perror("chdir: .. to %s", cwd);
                return "";
            }
        }
}