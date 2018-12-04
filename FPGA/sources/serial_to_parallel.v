module serial_to_parallel #(
        parameter DATA_SIZE = 8,
        parameter WIDTH     = 32,
        parameter COUNT     = 5
    ) (
        input  wire                 clk,
        input  wire                 rst,
        input  wire                 load,
        input  wire                 en,
        input  wire [DATA_SIZE-1:0] D,
        output reg  [WIDTH-1:0]     Q,
        output wire                 done
    );
    initial begin
        Q = {DATA_SIZE{1'b0}};
    end
    
    always @(posedge clk) begin
        if      (rst)  Q <= {DATA_SIZE{1'b0}};
        else if (load) Q <= {DATA_SIZE{1'b0}};
        else if (en)   Q <= Q << DATA_SIZE | D;
        else           Q <= Q;
    end

    down_counter # (
        .N          (COUNT),
        .WIDTH      ($clog2(COUNT) + 1)
    ) DN_COUNT (
        .clk        (clk),
        .rst        (rst),
        .load       (load),
        .en         (en),
        .zero       (done)
    );

endmodule