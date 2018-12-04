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

module uart_fpga (
        input  wire        clk100MHz,
        input  wire        rst,
        input  wire [1:0]  sel,
        input  wire        rx,
        output wire        tx,
        output wire [7:0]  LEDSEL,
        output wire [7:0]  LEDOUT
    );

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
        ) UART_WRAPPER (
            .clk            (clk100MHz),
            .rst            (rst),
            .tx             (tx),
            .rx             (rx),
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
            .Clk                    (clk100MHz),    // Clock
            .Rst                    (rst)     // Reset
        );

    reg [31:0] A_in;
    reg [31:0] B_in;
    reg [31:0] P_out;

    wire [3:0] hex[7:0];
    wire [7:0] s[7:0];

    wire clk_4sec;
    wire clk_5KHz;

    always @(posedge clk100MHz) begin
        if (rst)   begin
            A_in <= 32'b0;
            B_in <= 32'b0;
        end
        else if (Start) begin
            A_in <= A;
            B_in <= B;
        end
        else begin
            A_in <= A_in;
            B_in <= B_in;
        end
    end

    always @(negedge clk100MHz) begin
        if (rst)        P_out <= 32'b0;
        else if (Done)  P_out <= P;
        else            P_out <= P_out;
    end

    clk_gen CLK_GEN (
            .clk100MHz              (clk100MHz),
            .rst                    (rst),
            .clk_4sec               (clk_4sec),
            .clk_5KHz               (clk_5KHz)
        );

    mux4 #(32) HEX_SEL  (
            .sel                   (sel),
            .a                     (A_in),
            .b                     (B_in),
            .c                     (P_out),
            .d                     (32'b0),
            .y                     ({hex[7], hex[6], hex[5], hex[4], hex[3], hex[2], hex[1], hex[0]})
        );

    hex_to_7seg HEX0 (
            .HEX                       (hex[0]),
            .s                         (s[0])
        );

    hex_to_7seg HEX1 (
            .HEX                       (hex[1]),
            .s                         (s[1])
        );

    hex_to_7seg HEX2 (
            .HEX                       (hex[2]),
            .s                         (s[2])
        );

    hex_to_7seg HEX3 (
            .HEX                       (hex[3]),
            .s                         (s[3])
        );

    hex_to_7seg HEX4 (
            .HEX                       (hex[4]),
            .s                         (s[4])
        );

    hex_to_7seg HEX5 (
            .HEX                       (hex[5]),
            .s                         (s[5])
        );

    hex_to_7seg HEX6 (
            .HEX                       (hex[6]),
            .s                         (s[6])
        );

    hex_to_7seg HEX7 (
            .HEX                       (hex[7]),
            .s                         (s[7])
        );

    led_mux LED_MUX (
        .clk                        (clk_5KHz),
        .rst                        (rst),
        .LED7                       (s[7]),
        .LED6                       (s[6]),
        .LED5                       (s[5]),
        .LED4                       (s[4]),
        .LED3                       (s[3]),
        .LED2                       (s[2]),
        .LED1                       (s[1]),
        .LED0                       (s[0]),
        .LEDSEL                     (LEDSEL),
        .LEDOUT                     (LEDOUT)
    );

endmodule