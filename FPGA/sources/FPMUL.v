`timescale 1ns/1ps

module FPMUL (
        input   wire    [31:00] A,      // Operand 1
        input   wire    [31:00] B,      // Operand 2
        output  wire    [31:00] P,      // Product
        output  wire            OF,     // Product overflow flag
        output  wire            UF,     // Product underflow flag
        output  wire            NaNF,   // Product NaN flag
        output  wire            InfF,   // Product infinity flag
        output  wire            DNF,    // Product denormalized flag
        output  wire            ZF,     // Product zero flag
        input   wire            Start,  // Start operation
        output  wire            Done,   // Operation done
        input   wire            Clk,    // Clock
        input   wire            Rst     // Reset
    );
    reg     [2:0]   cnt;
    
    reg [31:00] A_in;
    reg [31:00] B_in;
    
    assign {OF, P} = A_in + B_in;
    assign ZF = (P == 32'b0) ? 1'b1 : 1'b0;
    
    assign {UF, NaNF, InfF, DNF} = 4'b01010;
    
    always@(posedge Clk)
    begin
             if (Rst)               begin cnt <= 0;A_in <= 32'b0; B_in <= 32'b0; end
        else if (Start)             begin cnt <= 1; A_in <= A; B_in <= B; end
        else if (cnt != 0)          cnt <= cnt + 1;
        else                        cnt <= 0;
    end
    
    assign Done = (cnt == 4);
    
endmodule
