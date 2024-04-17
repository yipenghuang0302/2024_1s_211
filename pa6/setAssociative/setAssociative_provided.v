input [2:0]  read_address;

input        set_0_line_0_valid;
input        set_0_line_0_tag;
input [15:0] set_0_line_0_block;

input        set_0_line_1_valid;
input        set_0_line_1_tag;
input [15:0] set_0_line_1_block;

input        set_1_line_0_valid;
input        set_1_line_0_tag;
input [15:0] set_1_line_0_block;

input        set_1_line_1_valid;
input        set_1_line_1_tag;
input [15:0] set_1_line_1_block;

output       read_hit;
output [7:0] read_byte;