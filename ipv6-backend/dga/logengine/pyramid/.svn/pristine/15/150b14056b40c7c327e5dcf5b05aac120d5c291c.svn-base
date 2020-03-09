#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include "dnspcap.h"

void usage (char *progname) {
    printf("Usage: %s [-i <interface>]\n", progname);
}

int main (int argc, char *argv[]) {
    
    char *pcapif = NULL;
    
    int c;
    while ((c = getopt(argc, argv, "hi:")) != -1) {
        switch (c) {
            case 'h':
                usage(argv[0]);
                exit(0);
            case 'i':
                pcapif = optarg;
                break;
        }
    }
    
    dnscache_init();
    
    dnspcap_start(pcapif);
    
    return 0;
}
