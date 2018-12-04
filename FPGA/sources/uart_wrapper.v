`define ENABLE       1'b1
`define NONE         0

module uart_wrapper #(
            parameter BAUD_RATE = 9600,             // 9600 Baud Rate
            parameter CLOCK_HZ  = 100 * (10 ** 6),  // Assume 100MHz Clock,
            parameter DATA_SIZE = 8,                // 5-8 Data Size
            parameter PARITY    = `NONE,            // No Parity, Even Parity, Odd Parity
            parameter STOP_SIZE = 1,                // Stop Size 1-2 Bits
            parameter TX_DEPTH  = 8,                // Tx Fifo Depth
            parameter RX_DEPTH  = 8,                // Rx Fifo Depth
            
            parameter TX_WIDTH = 32, // Tx Data Width
            parameter RX_WIDTH = 32, // Rx Data Width
            parameter TX_COUNT = 4,  // Number of Tx Transactions
            parameter RX_COUNT = 4   // Number of Rx Transactions
    ) (
        input  wire                clk,
        input  wire                rst,
        input  wire                rx,
        output wire                tx,
        input  wire                tx_rst,
        input  wire                tx_start,
        input  wire [TX_WIDTH-1:0] tx_data,
        input  wire                rx_rst,
        input  wire                rx_start,
        output wire [RX_WIDTH-1:0] rx_data,

        output wire                 tx_full,
        output wire                 tx_empty,
        output wire                 rx_full,
        output wire                 rx_empty
    );
    
    wire [DATA_SIZE-1:0] data;
    wire tx_done;
    wire rx_done;
    
    wire [DATA_SIZE-1:0] tx_q;
    wire [DATA_SIZE-1:0] rx_d;
    assign data    = (!tx_done) ? tx_q : {DATA_SIZE{1'bz}}; // Tx Data
    assign rx_d    = (tx_done)  ? data : {DATA_SIZE{1'bz}}; // Rx Data
    
    parallel_to_serial #(
            .DATA_SIZE      (DATA_SIZE),
            .WIDTH          (TX_WIDTH),
            .COUNT          (TX_COUNT)
        ) TX_P2S (
            .clk            (~clk),
            .rst            (tx_rst),
            .load           (tx_start),
            .en             (!tx_done),
            .D              (tx_data),
            .Q              (tx_q),
            .done           (tx_done)
        );

    serial_to_parallel #(
            .DATA_SIZE      (DATA_SIZE),
            .WIDTH          (RX_WIDTH),
            .COUNT          (RX_COUNT)
        ) RX_S2P (
            .clk            (~clk),
            .rst            (rx_rst),
            .load           (rx_start),
            .en             (!rx_done),
            .D              (rx_d),
            .Q              (rx_data),
            .done           (rx_done)
        );

    UART #(
            .BAUD_RATE       (BAUD_RATE),            
            .CLOCK_HZ        (CLOCK_HZ),
            .DATA_SIZE       (DATA_SIZE),
            .PARITY          (PARITY),
            .STOP_SIZE       (STOP_SIZE),
            .TX_DEPTH        (TX_DEPTH),
            .RX_DEPTH        (RX_DEPTH)
        ) UART (
            .clk             (clk),
            .rst             (rst),
            .cs              (!rx_done || !tx_done),
            .we              (!tx_done),
            .data            (data),
            .tx              (tx),
            .rx              (rx),
            .oe              (`ENABLE),
            .tx_full         (tx_full), 
            .tx_empty        (tx_empty),
            .rx_full         (rx_full), 
            .rx_empty        (rx_empty) 
        );

endmodule