module parallel_to_serial #(
        parameter DATA_SIZE = 8,
        parameter WIDTH     = 32,
        parameter COUNT     = 5
    ) (
        input  wire                 clk,
        input  wire                 rst,
        input  wire                 load,
        input  wire                 en,
        input  wire [WIDTH-1:0]     D,
        output wire [DATA_SIZE-1:0] Q,
        output wire                 done
    );
    
    reg [WIDTH-1:0] data;

    initial begin
        data = {DATA_SIZE{1'b0}};
    end

    always @(posedge clk) begin
        if      (rst)  data <= {DATA_SIZE{1'b0}};
        else if (load) data <= D;
        else if (en)   data <= data << DATA_SIZE;
        else           data <= data;
    end

    assign Q = data[WIDTH-1:WIDTH-8];


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