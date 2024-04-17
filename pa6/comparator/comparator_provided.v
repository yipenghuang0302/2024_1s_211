input [1:0] a;
input [1:0] b;

output equal;

wire bit_1_equal;
wire bit_0_equal;

assign bit_1_equal = a[1] ~^ b[1];
assign bit_0_equal = a[0] ~^ b[0];

assign equal = bit_1_equal & bit_0_equal;
