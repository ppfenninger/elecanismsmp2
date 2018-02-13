/*
** Copyright (c) 2018, Bradley A. Minch
** All rights reserved.
** Modified by Chloe Grubb Paige Pfenninger
*/

#include "elecanisms.h"
#include "usb.h"

#define ENC_MISO            D1
#define ENC_MOSI            D0
#define ENC_SCK             D2
#define ENC_CSn             D3

#define ENC_MISO_DIR        D1_DIR
#define ENC_MOSI_DIR        D0_DIR
#define ENC_SCK_DIR         D2_DIR
#define ENC_CSn_DIR         D3_DIR

#define ENC_MISO_RP         D1_RP
#define ENC_MOSI_RP         D0_RP
#define ENC_SCK_RP          D2_RP

#define ENC_READ_REG_AND_TIME        6

uint16_t even_parity(uint16_t v) {
    v ^= v >> 8;
    v ^= v >> 4;
    v ^= v >> 2;
    v ^= v >> 1;
    return v & 1;
}

WORD enc_readReg(WORD address) {
    WORD cmd, result;
    uint16_t temp;

    cmd.w = 0x4000 | address.w;         // set 2nd MSB to 1 for a read
    cmd.w |= even_parity(cmd.w) << 15;

    ENC_CSn = 0;

    SPI2BUF = (uint16_t)cmd.b[1];
    while (SPI2STATbits.SPIRBF == 0) {}
    temp = SPI2BUF;

    SPI2BUF = (uint16_t)cmd.b[0];
    while (SPI2STATbits.SPIRBF == 0) {}
    temp = SPI2BUF;

    ENC_CSn = 1;

    __asm__("nop");     // p.12 of the AS5048 datasheet specifies a minimum
    __asm__("nop");     //   high time of CSn between transmission of 350ns
    __asm__("nop");     //   which is 5.6 Tcy, so do nothing for 6 Tcy.
    __asm__("nop");
    __asm__("nop");
    __asm__("nop");

    ENC_CSn = 0;

    SPI2BUF = 0;
    while (SPI2STATbits.SPIRBF == 0) {}
    result.b[1] = (uint8_t)SPI2BUF;

    SPI2BUF = 0;
    while (SPI2STATbits.SPIRBF == 0) {}
    result.b[0] = (uint8_t)SPI2BUF;

    ENC_CSn = 1;

    return result;
}

void vendor_requests(void) {
    WORD temp, time1, time2; 
    uint16_t i;

    switch (USB_setup.bRequest) {
        case ENC_READ_REG_AND_TIME:
            temp = enc_readReg(USB_setup.wValue);
            time1.w = TMR2;
            time2.w = TMR3;

            if (SW1 == 0) {
                BD[EP0IN].address[0] = 0; //angle value
                BD[EP0IN].address[1] = 0; //angle value

                BD[EP0IN].address[2] = 0; // time value
                BD[EP0IN].address[3] = 0; // time value
                BD[EP0IN].address[4] = 0; // time value
                BD[EP0IN].address[5] = 0; // time value
                BD[EP0IN].bytecount = 6;
                BD[EP0IN].status = UOWN | DTS | DTSEN;
            }
            else {
                BD[EP0IN].address[0] = temp.b[0]; //angle value
                BD[EP0IN].address[1] = temp.b[1]; //angle value

                BD[EP0IN].address[2] = time1.b[0]; // time value
                BD[EP0IN].address[3] = time1.b[1]; // time value
                BD[EP0IN].address[4] = time2.b[0]; // time value
                BD[EP0IN].address[5] = time2.b[1]; // time value
                BD[EP0IN].bytecount = 6;
                BD[EP0IN].status = UOWN | DTS | DTSEN;
            }
            break;
        default:
            USB_error_flags |= REQUEST_ERROR;
    }
}

int16_t main(void) {
    uint8_t *RPOR, *RPINR;

    init_elecanisms();

    // //make a 32 bit timer
    T2CON = 0X30; //Stops any Timer2 operation
    T3CON = 0x30;
    TMR3 = 0x00;
    TMR2 = 0x00;  //Clears contents of timer2 register
    PR2 = 0xFFFF; //Loads the Period register2 with 0xFFFF
    PR3 = 0xFFFF;
    IPC2bits.T3IP = 0x01;
    IFS0bits.T3IF = 0;
    T2CONbits.T32 = 1;
    T2CONbits.TON = 1; //Enable 32-bit timer operation

    // Configure encoder pins and connect them to SPI2
    ENC_CSn_DIR = OUT; ENC_CSn = 1;
    ENC_SCK_DIR = OUT; ENC_SCK = 0;
    ENC_MOSI_DIR = OUT; ENC_MOSI = 0;
    ENC_MISO_DIR = IN;
    RPOR = (uint8_t *)&RPOR0;
    RPINR = (uint8_t *)&RPINR0;
    __builtin_write_OSCCONL(OSCCON & 0xBF);
    RPINR[MISO2_RP] = ENC_MISO_RP;
    RPOR[ENC_MOSI_RP] = MOSI2_RP;
    RPOR[ENC_SCK_RP] = SCK2OUT_RP;
    __builtin_write_OSCCONL(OSCCON | 0x40);
    SPI2CON1 = 0x003B;              // SPI2 mode = 1, SCK freq = 8 MHz
    SPI2CON2 = 0;
    SPI2STAT = 0x8000;
    

    // all of the motor stuff

    D8_DIR = OUT;      // configure D8 to be a digital output (IN1)
    D8 = 0;            // set D8 low (IN1)
    D7_DIR = OUT;      // configure D7 to be a digital output (IN2)
    D7 = 0;             // set D8 low (IN1)
    __builtin_write_OSCCONL(OSCCON & 0xBF);
    RPOR[D8_RP] = OC1_RP;  // connect the OC1 module output to pin D8
    __builtin_write_OSCCONL(OSCCON | 0x40);
    OC1CON1 = 0x1C06;   // configure OC1 module to use the peripheral clock (i.e., FCY, OCTSEL<2:0> = 0b111) and to operate in edge-aligned PWM mode (OCM<2:0> = 0b110)
    OC1CON2 = 0x001F;   // configure OC1 module to syncrhonize to itself  (i.e., OCTRIG = 0 and SYNCSEL<4:0> = 0b11111)
    OC1RS = (uint16_t)(FCY / 1e4 - 1.);     // configure period register to get a frequency of 1kHz
    OC1R = 0; //configure duty cycle to 0%
    OC1TMR = 0;
    

    USB_setup_vendor_callback = vendor_requests;
    init_usb();


    while (USB_USWSTAT != CONFIG_STATE) {
        #ifndef USB_INTERRUPT
                usb_service();
        #endif
    }

    while (1) {
        if (SW1 == 0){
            OC1R = OC1RS; //sets duty cycle to 100%
        }  
        else {
            OC1R = 0;
        } 
        #ifndef USB_INTERRUPT
                usb_service();
        #endif
    }
}

