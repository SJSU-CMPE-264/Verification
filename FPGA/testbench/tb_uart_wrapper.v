`define ENABLE       1'b1
`define NONE         0
`define EVEN         1
`define ODD          2
`define DATA_SIZE    8

`define START_WIDTH   1
`define A_WIDTH       32
`define B_WIDTH       32
`define PRODUCT_WIDTH 32
`define OF_WIDTH      1
`define UF_WIDTH      1
`define NANF_WIDTH    1
`define INFF_WIDTH    1
`define DNF_WIDTH     1
`define ZF_WIDTH      1

`define TX_WIDTH (`PRODUCT_WIDTH + `OF_WIDTH + `UF_WIDTH + `NANF_WIDTH + `INFF_WIDTH + `DNF_WIDTH + `ZF_WIDTH)
`define RX_WIDTH (`START_WIDTH + `A_WIDTH + `B_WIDTH)

`define TX_WIDTH_PADDING (`DATA_SIZE - (`TX_WIDTH % 8))
`define RX_WIDTH_PADDING (`DATA_SIZE - ((`RX_WIDTH) % 8))

`define TX_TOTAL_WIDTH (`TX_WIDTH + `TX_WIDTH_PADDING)
`define RX_TOTAL_WIDTH (`RX_WIDTH + `RX_WIDTH_PADDING)

`define TX_COUNT (`TX_TOTAL_WIDTH / `DATA_SIZE)
`define RX_COUNT (`RX_TOTAL_WIDTH / `DATA_SIZE)

`define BAUD_RATE 115200            // 115200 Baud Rate
`define CLOCK_HZ  100 * (10 ** 6)   // 100MHz Clock
`define STOP_SIZE 1

`define TX_DEPTH  `TX_COUNT
`define RX_DEPTH  `RX_COUNT

module tb_uart_wrapper;
    wire tb_tx;
    wire tb_rx;
    
    wire tx_full;
    wire tx_empty;
    wire rx_full;
    wire rx_empty;


    wire [31:00] A;
    wire [31:00] B;
    wire [31:00] P;
    wire         OF;
    wire         UF;
    wire         NaNF;
    wire         InfF;
    wire         DNF;
    wire         ZF;
    wire         Start;
    wire         Done;
    reg          clk;
    reg          rst;

    reg  [31:00] tb_A;
    reg  [31:00] tb_B;
    reg          tb_Start;

    reg          tb_start;
    reg [7:0]    tb_data;
    wire         tb_ready;
    
    reg  [`RX_TOTAL_WIDTH-1:0] data;

    integer I;

    task tick;
    begin
        clk = 1'b0; #5
        clk = 1'b1; #5
        clk = 1'b0;
    end
    endtask

    UART_TX #(
            .BAUD_RATE      (`BAUD_RATE),
            .CLOCK_HZ       (`CLOCK_HZ),
            .DATA_SIZE      (`DATA_SIZE),
            .PARITY         (`NONE),
            .STOP_SIZE      (`STOP_SIZE)
        ) TX (
            .clk            (clk),
            .start          (tb_start),
            .data           (tb_data),
            .tx             (tb_tx),
            .ready          (tb_ready)
        );
    
    uart_wrapper #(
            .BAUD_RATE      (`BAUD_RATE),
            .CLOCK_HZ       (`CLOCK_HZ),
            .DATA_SIZE      (`DATA_SIZE),
            .PARITY         (`NONE),
            .STOP_SIZE      (`STOP_SIZE),
            .TX_DEPTH       (`TX_DEPTH),
            .RX_DEPTH       (`RX_DEPTH),
            
            .TX_WIDTH       (`TX_TOTAL_WIDTH),
            .RX_WIDTH       (`RX_TOTAL_WIDTH),
            .TX_COUNT       (`TX_COUNT),
            .RX_COUNT       (`RX_COUNT)
        ) DUT (
            .clk            (clk),
            .rst            (rst),
            .tx             (tb_rx),
            .rx             (tb_tx),
            .tx_rst         (1'b0),
            .tx_start       (Done),
            .tx_data        ({OF, UF, NaNF, InfF, DNF, ZF, P}),
            .rx_rst         (Start),
            .rx_start       (rx_full),
            .rx_data        ({Start, A, B}),
            .tx_full        (tx_full), 
            .tx_empty       (tx_empty),
            .rx_full        (rx_full), 
            .rx_empty       (rx_empty) 
        );
        
    FPMUL FPMUL (
                .A                      (A),      // Operand 1
                .B                      (B),      // Operand 2
                .P                      (P),      // Product
                .OF                     (OF),     // Product overflow flag
                .UF                     (UF),     // Product underflow flag
                .NaNF                   (NaNF),   // Product NaN flag
                .InfF                   (InfF),   // Product infinity flag
                .DNF                    (DNF),    // Product denormalized flag
                .ZF                     (ZF),     // Product zero flag
                .Start                  (Start),  // Start operation
                .Done                   (Done),   // Operation done
                .Clk                    (clk),    // Clock
                .Rst                    (rst)     // Reset
            );
    initial begin
        rst = 1'b0; #2
        rst = 1'b1; #2
        rst = 1'b0; #1

        tb_A = 32'h01234567;
        tb_B = 32'h89ABCDEF;
        tb_Start = 1'b1;
        data = {tb_Start, tb_A, tb_B};
        #5;
        for(I = 0; I < `RX_COUNT; I = I + 1) begin
            tb_data = data[`RX_TOTAL_WIDTH-1:`RX_TOTAL_WIDTH-8];
            data    = data << 8;
            tb_start = 1'b1;
            tick;
            tb_start = 1'b0;
            while(!tb_ready) tick;
        end
        
        
        tb_A = 32'h89ABCDEF;
        tb_B = 32'h01234567;
        tb_Start = 1'b1;
        data = {tb_Start, tb_A, tb_B};
        #5;
        for(I = 0; I < `RX_COUNT; I = I + 1) begin
            tb_data = data[`RX_TOTAL_WIDTH-1:`RX_TOTAL_WIDTH-8];
            data    = data << 8;
            tb_start = 1'b1;
            tick;
            tb_start = 1'b0;
            while(!tb_ready) tick;
        end
        
        $display("End simulation");
        
        $finish;
    end   

endmodule