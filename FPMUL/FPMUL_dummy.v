`timescale 1ns/1ps

module FPMUL (
    input   wire    [31:00] A,      // Operand 1
    input   wire    [31:00] B,      // Operand 2
    output  reg     [31:00] P,      // Product
    output  reg             OF,     // Product overflow flag
    output  reg             UF,     // Product underflow flag
    output  reg             NaNF,   // Product NaN flag
    output  reg             InfF,   // Product infinity flag
    output  reg             DNF,    // Product denormalized flag
    output  reg             ZF,     // Product zero flag
    input   wire            Start,  // Start operation
    output  reg             Done,   // Operation done
    input   wire            Clk,    // Clock
    input   wire            Rst    // Reset
);
    reg     [2:0]   cnt; 

    initial
    begin
        P = 32'h80000000;
        cnt = 0;
        OF = 0;
        UF = 0;
        NaNF = 0;
        InfF = 0;
        DNF = 0;
        ZF = 1;
        Done = 0;
    end
    
    always@(posedge Clk)
    begin
             if (Rst)               begin cnt = 0; Done = 0; end
        else if (Start && cnt == 0) cnt = 1;
        else if (cnt < 4)           cnt = cnt + 1;
        else if (cnt >= 4)          Done = 1;
    end
    
endmodule
