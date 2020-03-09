#ifndef __DNSFILE_H_
#define __DNSFILE_H_

#include <stdlib.h>
#include <string.h>
#include <stdint.h>

FILE *file_rr = NULL;
uint32_t time_rr = 0;

FILE *dnsfile_rr () {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 3600;
    if (file_rr == NULL || now.tv_sec != time_rr) {
        time_rr = now.tv_sec;
        if (file_rr != NULL) {
            fclose(file_rr);
            file_rr = NULL;
        }
        char filename[32];
        struct tm *now_tm = localtime(&(now.tv_sec));
        strftime(filename, sizeof filename, "rr_%Y%m%d_%H.log", now_tm);
        fprintf(stdout, "Opening log file: %s\n", filename);
        file_rr = fopen(filename, "a");
        if (file_rr == NULL) {
            fprintf(stderr, "Error: Unable to open file for appending: %s\n", filename);
            return stdout;
        }
    }
    return file_rr;
}


#endif //__DNSFILE_H_

