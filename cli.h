#include "pid.h"

void init_cli();
void command_loop(struct PID_DATA *piddata);
uint16_t get_word();
void put_word(uint16_t w);
