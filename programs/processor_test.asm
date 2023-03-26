// Memory instruction testing
LB A 00
LB B 01
SB A 02
SB B 03
LB A 03
LB B 02

// ALU operation testing
ADD A
ADD B
SUB B
SUB A
MUL A
MUL B
SLA A
SRA A
SLA B
SRA B
INC A A
DEC A A
INC B B
DEC B B
SEQ A
SEQ B
SEQ A
SGT A
SLT A
SEQ B
SLT B
SGT B
INC B B
COPY B
COPY A

// Conditional branch testing
        BEQ LABEL1
        LB A 00
LABEL1: BLT LABEL2
        LB A 00
LABEL2: BGT LABEL3
        LB A 01
LABEL3: LB B 01

// Unconditional branch
JUMP LABEL4
SLA A

// Go to idle state and wait for Interrupts
LABEL4: IDLE

// Functional call testing
MOUSE_START: FUNC FUNC1

// Register dereference testing
DEREF A
DEREF B

// Extra feature testing: bitwise ALU operands
AND A
XOR A
NOT B
AND B
OR B
NOT A
XOR B
OR A

// Supposed end of file functions
FUNC1: RETURN
MOUSE: JUMP MOUSE_START