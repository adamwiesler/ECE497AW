// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Read one gpio pin and write it out to another using mmap.
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
// Modified again by Adam Wiesler 25-Sept-2017 to be able to control/monitor two GPIO ports

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
    printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}

int main(int argc, char *argv[]) {
    volatile void *gpio_addr_0;
    volatile unsigned int *gpio_oe_addr_0;
    volatile unsigned int *gpio_datain_0;
    volatile unsigned int *gpio_setdataout_addr_0;
    volatile unsigned int *gpio_cleardataout_addr_0;


    volatile void *gpio_addr_1;
    volatile unsigned int *gpio_oe_addr_1;
    volatile unsigned int *gpio_datain_1;
    volatile unsigned int *gpio_setdataout_addr_1;
    volatile unsigned int *gpio_cleardataout_addr_1;

    unsigned int reg;

    // Set the signal callback for Ctrl-C
    signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    printf("Mapping %X - %X (size: %X)\n", GPIO2_START_ADDR, GPIO2_END_ADDR, 
                                           GPIO2_SIZE);

    gpio_addr_0 = mmap(0, GPIO2_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO2_START_ADDR);

    gpio_oe_addr_0           = gpio_addr_0 + GPIO_OE;
    gpio_datain_0            = gpio_addr_0 + GPIO_DATAIN;
    gpio_setdataout_addr_0   = gpio_addr_0 + GPIO_SETDATAOUT;
    gpio_cleardataout_addr_0 = gpio_addr_0 + GPIO_CLEARDATAOUT;

    if(gpio_addr_0 == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }


    printf("Mapping %X - %X (size: %X)\n", GPIO1_START_ADDR, GPIO1_END_ADDR, 
                                           GPIO1_SIZE);

    gpio_addr_1 = mmap(0, GPIO3_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO3_START_ADDR);

    gpio_oe_addr_1           = gpio_addr_1 + GPIO_OE;
    gpio_datain_1            = gpio_addr_1 + GPIO_DATAIN;
    gpio_setdataout_addr_1   = gpio_addr_1 + GPIO_SETDATAOUT;
    gpio_cleardataout_addr_1 = gpio_addr_1 + GPIO_CLEARDATAOUT;

    if(gpio_addr_1 == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }




    printf("Copying PAUSE button and GP0_3 to RED and GREEN LEDs on BBBlue\n");
    while(keepgoing) {
    	if(*gpio_datain_0 & PAUSE) {
            *gpio_setdataout_addr_0= LEDGREEN;
    	} else {
            *gpio_cleardataout_addr_0 = LEDGREEN;
    	}


    	if(*gpio_datain_1 & GP1_3) {
            *gpio_setdataout_addr_0= LEDRED;
    	} else {
            *gpio_cleardataout_addr_0 = LEDRED;
    	}

        //usleep(1);
    }

    munmap((void *)gpio_addr_0, GPIO2_SIZE);
    munmap((void *)gpio_addr_1, GPIO1_SIZE);
    close(fd);
    return 0;
}
