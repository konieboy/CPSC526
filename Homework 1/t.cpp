#include <cstdlib>
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <linux/if_packet.h>
#include <linux/if_ether.h>

#define PCKT_LEN 8192
#define SOURCEPORT "52522" // Client Port 
#define DESTPORT "35143" // the port client will be connecting to 

#define SOURCEIP "127.0.0.1" // the client ip 
#define DESTIP "127.0.1.1" // the Server IP

unsigned short csum(unsigned short *buf, int len) {
    unsigned long sum;
    for(sum=0; len>0; len--)
        sum += *buf++;
    sum = (sum >> 16) + (sum &0xffff);
    sum += (sum >> 16);
    return (unsigned short)(~sum);
}

int main(int argc, char** argv) {

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

    sin.sin_family = AF_INET;           // Address family
    sin.sin_port = htons(atoi(SOURCEPORT)); // Source port
    inet_pton(AF_INET, DESTIP, &(sin.sin_addr.s_addr)); // Dest IP - ERROR WAS WRONG IP

    ip->ihl = 5;
    ip->version = 4;
    ip->tos = 16;
    ip->tot_len = sizeof(class iphdr) + sizeof(class tcphdr);
    ip->id = htons(54321);
    ip->frag_off = 0;
    ip->ttl = 32;
    ip->protocol = 6; // TCP
    ip->check = 0; // Done by kernel
    inet_pton(AF_INET, SOURCEIP, &(ip->saddr)); // Source IP
    inet_pton(AF_INET, DESTIP, &(ip->daddr)); // Destination IP

    // The TCP structure
    tcp->source = htons(atoi(SOURCEPORT));
    tcp->dest = htons(atoi(DESTPORT));      // Destination port
    tcp->seq = htonl(1);
    tcp->ack_seq = 0;
    tcp->doff = 5;
    tcp->syn = 1; // send syn packet
    tcp->ack = 0;
    
    //tcp->window = htons(43690);
    tcp->window = htons(32767);

    tcp->check = 0; // Done by kernel
    tcp->rst = 0;
    tcp->urg_ptr = 0;

    ip->check = csum((unsigned short *) buffer, (sizeof(class iphdr) + sizeof(class tcphdr)));

    // Bind socket to interface
    int iface = 1;
    const int *val = &iface;
    char *opt = "lo";
    if(setsockopt(sd, IPPROTO_IP, IP_HDRINCL, val, sizeof(iface)) < 0) {
    //if(setsockopt(sd, SOL_SOCKET, SO_BINDTODEVICE, opt, 4) < 0) {
        perror("setsockopt() error");
        exit(-1);
    }
    else
        printf("setsockopt() is OK\n");

    if(sendto(sd, buffer, ip->tot_len, 0, (sockaddr*)&sin, sizeof(class sockaddr_in)) < 0) {
       perror("sendto() error");
       exit(-1);
    }
    else
        printf("Send OK!");

    close(sd);
    return 0;
}