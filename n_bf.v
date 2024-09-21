module n_bf(input signed[15:0] a, //a
          input signed [15:0] b, //b
          input signed [15:0] c,//c 
          input signed [15:0] d,//d
          input signed [15:0] w_r,
          input signed [15:0] w_i,
          output signed [15:0] out1_r,
          output signed [15:0] out1_i,
          output signed [15:0] out2_r,
          output signed [15:0] out2_i
          );

      wire signed [15:0] t_r, t_i;
      
      wire signed [31:0] prod_r, prod_i;
      
      wire signed [31:0] tr_wr, ti_wi;
      wire signed [31:0] ti_wr, tr_wi;
      
      assign out1_r = a + c;
      assign out1_i = b + d;
      
      assign t_r = a - c;
      assign t_i = b - d;
      
      n_mult m1(.A(t_r), .B(w_r), .product(tr_wr));
      n_mult m2(.A(t_i), .B(w_i), .product(ti_wi));
      n_mult m3(.A(t_r), .B(w_i), .product(tr_wi));
      n_mult m4(.A(t_i), .B(w_r), .product(ti_wr));
      
      assign prod_r = tr_wr - ti_wi;
      assign prod_i = tr_wi + ti_wr;
      
      assign out2_r = prod_r[23:8];
      assign out2_i = prod_i[23:8];

endmodule
