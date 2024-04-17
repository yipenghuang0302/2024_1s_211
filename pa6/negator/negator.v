input [7:0] a;

output [7:0] b;

wire inv_a_7;
wire inv_a_6;
wire inv_a_5;
wire inv_a_4;
wire inv_a_3;
wire inv_a_2;
wire inv_a_1;
wire inv_a_0;

wire carry_0;
wire carry_1;
wire carry_2;
wire carry_3;
wire carry_4;
wire carry_5;
wire carry_6;
wire carry_7;

assign inv_a_7 = ~ a[7];
assign inv_a_6 = ~ a[6];
assign inv_a_5 = ~ a[5];
assign inv_a_4 = ~ a[4];
assign inv_a_3 = ~ a[3];
assign inv_a_2 = ~ a[2];
assign inv_a_1 = ~ a[1];
assign inv_a_0 = ~ a[0];

assign carry_0 = inv_a_0;
assign carry_1 = carry_0 & inv_a_1;
assign carry_2 = carry_1 & inv_a_2;
assign carry_3 = carry_2 & inv_a_3;
assign carry_4 = carry_3 & inv_a_4;
assign carry_5 = carry_4 & inv_a_5;
assign carry_6 = carry_5 & inv_a_6;
assign carry_7 = carry_6 & inv_a_7;

assign b[0] = ~ inv_a_0;
assign b[1] = carry_0 ^ inv_a_1;
assign b[2] = carry_1 ^ inv_a_2;
assign b[3] = carry_2 ^ inv_a_3;
assign b[4] = carry_3 ^ inv_a_4;
assign b[5] = carry_4 ^ inv_a_5;
assign b[6] = carry_5 ^ inv_a_6;
assign b[7] = carry_6 ^ inv_a_7;
