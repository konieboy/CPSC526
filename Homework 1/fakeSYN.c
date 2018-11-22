#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>

// Get ip and tcp structure
#include <netinet/ip.h>
#include <netinet/tcp.h>

#include <arpa/inet.h>

#define PORT "35143" // the port client will be connecting to 

#define MAXDATASIZE 100 // max number of bytes we can get at once 


struct pseudo_header {
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(int argc, char *argv[])
{

    char *buffer = new char[PCKT_LEN]();

    class iphdr *ip = (struct iphdr *) buffer;
    class tcphdr *tcp = (struct tcphdr *) (buffer + sizeof(struct iphdr));

    class sockaddr_in sin;

    int sd = socket(PF_INET, SOCK_RAW, IPPROTO_TCP);
    if(sd < 0) {
       perror("socket() error");
       exit(-1);
    } else {
        printf("socket()-SOCK_RAW and tcp protocol is OK.\n");
    }


    // int sockfd, numbytes;  
    // char buf[MAXDATASIZE];
    // struct addrinfo hints, *servinfo, *p;
    // int rv;
    // char s[INET6_ADDRSTRLEN];


    // char hostname[100];

    // int error = gethostname(hostname, 100);


    // printf("\nThe hostname is: %s\n", hostname);

    // // if (argc != 2) {
    // //     fprintf(stderr,"usage: client hostname\n");
    // //     exit(1);
    // // }

    // memset(&hints, 0, sizeof hints);
    // hints.ai_family = AF_UNSPEC;
    // hints.ai_socktype = SOCK_STREAM;

    // if ((rv = getaddrinfo(hostname, PORT, &hints, &servinfo)) != 0) 
    // {
    //     fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
	// 	exit(1);
    // }

    // // Create Raw Socket
	// if ((sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)) == -1) {
	// 	printf("Socket was not created properly");
	// 	exit(1);
	// }

	// char datagram[4096];
	// memset(datagram,0,4096);

    // // loop through all the results and connect to the first we can
    // for(p = servinfo; p != NULL; p = p->ai_next) {
    //     if ((sockfd = socket(p->ai_family, p->ai_socktype,
    //             p->ai_protocol)) == -1) {
    //         perror("client: socket");
    //         continue;
    //     }

    //     if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
    //         close(sockfd);
    //         perror("client: connect");
    //         continue;
    //     }

    //     break;
    // }

    // if (p == NULL) {
    //     fprintf(stderr, "client: failed to connect\n");
    //     return 2;
    // }

    // inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
    //         s, sizeof s);
    // printf("client: connecting to %s\n", s);

    // freeaddrinfo(servinfo); // all done with this structure

    // if ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) == -1) {
    //     perror("recv");
    //     exit(1);
    // }

    // buf[numbytes] = '\0';

    // printf("client: received '%s'\n",buf);

    // close(sockfd);

    // return 0;
}