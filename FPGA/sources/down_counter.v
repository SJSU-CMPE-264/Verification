module down_counter # (
        parameter N     = 4,
        parameter WIDTH = 3
    ) (
        input  wire             clk,
        input  wire             rst,
        input  wire             load,
        input  wire             en,
        output reg  [WIDTH-1:0] count,
        output wire             zero
    );
    
    initial begin
        count = {WIDTH{1'b0}};
    end

    always @ (posedge clk or posedge rst) begin
        if      (rst)  count <= {WIDTH{1'b0}};
        else if (load) count <= N;
        else if (en)   count <= count - 1;
        else           count <= count;
    end

    assign zero = (count == {WIDTH-1{1'b0}}) ? 1'b1 : 1'b0;

endmodule

