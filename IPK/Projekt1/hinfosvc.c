/*
 * IPK.2022L
 *
 * Project 1 - Simple Server communicating by HTTP protocol
 *
 * Matus Vrablik (xvrabl05@fit.vutbr.cz)
 *
 */
#define _XOPEN_SOURCE 500
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<unistd.h>

float GetCPULoad() {
	FILE* FileHandler;
	char FileBuffer[1024];
	long long Puser,Pnice,Psystem,Pidle,Piowait,Pirq,Psoftirq,Psteal,Pguest,Pguest_nice=0;
	long long Nuser,Nnice,Nsystem,Nidle,Niowait,Nirq,Nsoftirq,Nsteal,Nguest,Nguest_nice=0;
	FileHandler = popen("cat /proc/stat|grep \"cpu\"|head -n 1| cut -d \" \" -f 2-", "r");
	if(FileHandler == NULL) {
		return -1; }
	fread(FileBuffer, sizeof(FileBuffer) - 1, 10, FileHandler);
	sscanf(FileBuffer, "%lld %lld %lld %lld %lld %lld %lld %lld %lld %lld\n",&Puser,&Pnice,&Psystem,&Pidle,&Piowait,&Pirq,&Psoftirq,&Psteal,&Pguest,&Pguest_nice); 
	fclose(FileHandler);
    sleep(1);
    FileHandler = NULL;
    memset(FileBuffer,0,1024);
    FileHandler = popen("cat /proc/stat|grep \"cpu\"|head -n 1|cut -d \" \" -f 2-", "r");
	if(FileHandler == NULL) {
		return -1; }
	fread(FileBuffer, sizeof(FileBuffer) - 1, 10, FileHandler);
	sscanf(FileBuffer, "%lld %lld %lld %lld %lld %lld %lld %lld %lld %lld\n",&Nuser,&Nnice,&Nsystem,&Nidle,&Niowait,&Nirq,&Nsoftirq,&Nsteal,&Nguest,&Nguest_nice);
	fclose(FileHandler);
    long long PrevIdle = Pidle + Piowait;
    long long Idle = Nidle + Niowait;
    long long PrevNonIdle = Puser + Pnice + Psystem + Pirq + Psoftirq + Psteal;
    long long NonIdle = Nuser + Nnice + Nsystem + Nirq + Nsoftirq + Nsteal;
    long long PrevTotal = PrevIdle + PrevNonIdle;
    long long Total = Idle + NonIdle;
    long long totald = Total - PrevTotal;
    long long idled = Idle - PrevIdle;
    long long cpuperc = totald - idled;
    float CPU_Percentage = (float)cpuperc/totald*100;
	return CPU_Percentage;
}
char* GetHostname(){
    FILE *FileHandler;
    char FileBuffer[1024] = "";
    char* hostname = malloc(sizeof(char*));
    if(hostname == NULL){
        return NULL;
    }

    FileHandler = fopen("/proc/sys/kernel/hostname", "r");
    if(FileHandler == NULL){
        return NULL;
    }
    fread(FileBuffer, sizeof(FileBuffer) - 1, 1, FileHandler);
    sscanf(FileBuffer, "%s", hostname);
    hostname = FileBuffer;
    fclose(FileHandler);

    return hostname;
}
char* GetCPUname(){
    FILE *FileHandler;
    char FileBuffer[1024] = "";
    char* cpuname = malloc(sizeof(char*));
    if(cpuname == NULL){
        return NULL;
    }
    FileHandler = popen("cat /proc/cpuinfo|grep \"model name\"|head -n 1 |cut -d \" \" -f 3-","r");
    if(FileHandler == NULL){
        return NULL;
    }
    fread(FileBuffer, sizeof(FileBuffer) -1, 1, FileHandler);
    sscanf(FileBuffer, "%s", cpuname);
    cpuname = FileBuffer;
    fclose(FileHandler);
    return cpuname;
}
int main(int argc,const char* argv[]){
	int welcome_socket;
	struct sockaddr_in sa;
	struct sockaddr_in sa_client;
    int port_number;
    
    if (argc != 2) {
       fprintf(stderr,"usage: %s <port>\n", argv[0]);
       exit(EXIT_FAILURE);
    }
    port_number = atoi(argv[1]);
    
    
	socklen_t sa_client_len=sizeof(sa_client);
	if ((welcome_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
	{
		perror("ERROR: socket");
		exit(EXIT_FAILURE);
	}
	
    int enable = 1;
    if (setsockopt(welcome_socket, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable)) < 0){
        fprintf(stderr,"setsockopt(SO_REUSEADDR) FAILED");
    }
    #ifdef SO_REUSEPORT
        if (setsockopt(welcome_socket, SOL_SOCKET, SO_REUSEPORT, &enable, sizeof(enable)) < 0)
            fprintf(stderr,"setsockopt(SO_REUSEPORT) FAILED");
    #endif
    
	memset(&sa,0,sizeof(sa));
	sa.sin_family = AF_INET;
	sa.sin_addr.s_addr = htonl(INADDR_ANY);
	sa.sin_port = htons(port_number);

	if ((bind(welcome_socket, (struct sockaddr*)&sa, sizeof(sa))) < 0)
	{
		perror("ERROR: bind");
		exit(EXIT_FAILURE);		
	}
	if ((listen(welcome_socket, 1)) < 0)
	{
		perror("ERROR: listen");
		exit(EXIT_FAILURE);				
	}
	while(1)
	{
		int comm_socket = accept(welcome_socket, (struct sockaddr*)&sa_client, &sa_client_len);		
		if (comm_socket > 0){			
			char buff[1024];
			int res = 0;
			res = recv(comm_socket, buff, 1024,0);
            if (res <= 0)                
                break;
                                            			
			
            char* call = strtok(buff, " ");
            if(strcmp(buff, "GET")){
                memset(buff, 0, 1024);
                sprintf(buff, "HTTP/1.1 400 Bad Request\r\n\r\nError 400 Bad Request\n");
            }
            else{
                call = strtok(NULL, " ");
                if(strcmp(call, "/hostname") == 0){
                    memset(buff, 0, 1024);
                    sprintf(buff, "HTTP/1.1 200 OK\r\nContent-Type: text/plain;\r\n\r\n%s",GetHostname());
                }
                else if(strcmp(call, "/cpu-name") == 0){
                    memset(buff, 0, 1024);
                    sprintf(buff, "HTTP/1.1 200 OK\r\nContent-Type: text/plain;\r\n\r\n%s",GetCPUname());
                }
                else if(strcmp(call, "/load") == 0){
                    memset(buff, 0, 1024);
                    sprintf(buff, "HTTP/1.1 200 OK\r\nContent-Type: text/plain;\r\n\r\n%.2f%%\n",GetCPULoad());
                }
                else{
                    memset(buff, 0, 1024);
                    sprintf(buff, "HTTP/1.1 400 Bad Request\r\n\r\nError 400 Bad Request\n");
                }
            }
            
			send(comm_socket, buff, strlen(buff), 0);
		}
		close(comm_socket);
	}	
}