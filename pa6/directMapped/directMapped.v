input  [1:0] read_address;

input        set_0_valid;
input        set_0_tag;
input  [7:0] set_0_block;

input        set_1_valid;
input        set_1_tag;
input  [7:0] set_1_block;

output       read_hit;
output [7:0] read_byte;

wire set_0_select;
wire set_1_select;

wire set_0_valid_select;
wire set_1_valid_select;
wire valid;

wire set_0_tag_select;
wire set_1_tag_select;
wire tag;

wire match;
wire read_hit;

wire set_0_block_07_select;
wire set_0_block_06_select;
wire set_0_block_05_select;
wire set_0_block_04_select;
wire set_0_block_03_select;
wire set_0_block_02_select;
wire set_0_block_01_select;
wire set_0_block_00_select;

wire set_1_block_07_select;
wire set_1_block_06_select;
wire set_1_block_05_select;
wire set_1_block_04_select;
wire set_1_block_03_select;
wire set_1_block_02_select;
wire set_1_block_01_select;
wire set_1_block_00_select;

wire block_07;
wire block_06;
wire block_05;
wire block_04;
wire block_03;
wire block_02;
wire block_01;
wire block_00;

assign set_0_select = ~ read_address[0];
assign set_1_select =   read_address[0];

assign set_0_valid_select = set_0_select & set_0_valid;
assign set_1_valid_select = set_1_select & set_1_valid;
assign valid = set_0_valid_select | set_1_valid_select;

assign set_0_tag_select = set_0_select & set_0_tag;
assign set_1_tag_select = set_1_select & set_1_tag;
assign tag = set_0_tag_select | set_1_tag_select;

assign match = read_address[1] ~^ tag;
assign read_hit = valid & match;

assign set_0_block_07_select = set_0_select & set_0_block[7];
assign set_0_block_06_select = set_0_select & set_0_block[6];
assign set_0_block_05_select = set_0_select & set_0_block[5];
assign set_0_block_04_select = set_0_select & set_0_block[4];
assign set_0_block_03_select = set_0_select & set_0_block[3];
assign set_0_block_02_select = set_0_select & set_0_block[2];
assign set_0_block_01_select = set_0_select & set_0_block[1];
assign set_0_block_00_select = set_0_select & set_0_block[0];

assign set_1_block_07_select = set_1_select & set_1_block[7];
assign set_1_block_06_select = set_1_select & set_1_block[6];
assign set_1_block_05_select = set_1_select & set_1_block[5];
assign set_1_block_04_select = set_1_select & set_1_block[4];
assign set_1_block_03_select = set_1_select & set_1_block[3];
assign set_1_block_02_select = set_1_select & set_1_block[2];
assign set_1_block_01_select = set_1_select & set_1_block[1];
assign set_1_block_00_select = set_1_select & set_1_block[0];

assign block_07 = set_0_block_07_select | set_1_block_07_select;
assign block_06 = set_0_block_06_select | set_1_block_06_select;
assign block_05 = set_0_block_05_select | set_1_block_05_select;
assign block_04 = set_0_block_04_select | set_1_block_04_select;
assign block_03 = set_0_block_03_select | set_1_block_03_select;
assign block_02 = set_0_block_02_select | set_1_block_02_select;
assign block_01 = set_0_block_01_select | set_1_block_01_select;
assign block_00 = set_0_block_00_select | set_1_block_00_select;

assign read_byte[7] = match & block_07;
assign read_byte[6] = match & block_06;
assign read_byte[5] = match & block_05;
assign read_byte[4] = match & block_04;
assign read_byte[3] = match & block_03;
assign read_byte[2] = match & block_02;
assign read_byte[1] = match & block_01;
assign read_byte[0] = match & block_00;
