# a1u_input

By Sungho Lee (sungholee3526@gmail.com)

## Hardware

Pins on 12-pin box header on the encoder boarder is numbered as below with the
orientation key at the top.

| <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> |
|----------|----------|----------|----------|----------|----------|
| 11       | 9        | 7        | 5        | 3        | 1        |
| 12       | 10       | 8        | 6        | 4        | 2        |

| Pin | Description        |
|-----|--------------------|
| 1   | Speaker (UNUSED)   |
| 2   | Speaker (UNUSED)   |
| 3   | GND                |
| 4   | GND                |
| 5   | UART RX (3.3V)     |
| 6   | UART TX (3.3V)     |
| 7   | VCC (3.3V)         |
| 8   | GND                |
| 9   | Trackball (UNUSED) |
| 10  | Trackball (UNUSED) |
| 11  | Power Switch On    |
| 12  | GND                |

Remember `RX` connects to host `TX` and `TX` connects to host `RX`.

Power off signal is carried through serial data and is not exposed on the box
header.

## Data Format

### Host to Encoder

Host sends three bytes to request data.

`A6 01 00`

### Encoder to Host

Encoder responds to the poll request with 18 byte data.

| 0    | 1    | 2              | 3    | 4           | 5          | 6    | 7    | 8           | 9          | 10   | 11   | 12          | 13         | 14   | 15   | 16          | 17         |
|------|------|----------------|------|-------------|------------|------|------|-------------|------------|------|------|-------------|------------|------|------|-------------|------------|
| `a7` | `10` | System Buttons | `01` | P1 Joystick | P1 Buttons | `00` | `02` | P2 Joystick | P2 Buttons | `00` | `03` | P3 Joystick | P3 Buttons | `00` | `04` | P4 Joystick | P4 Buttons |

#### System Buttons

| 0   | 1   | 2   | 3     | 4       | 5       | 6        | 7        |
|-----|-----|-----|-------|---------|---------|----------|----------|
| `0` | `0` | `0` | Live! | Power 0 | Power 1 | Volume 0 | Volume 1 |

#### Joystick

| 0   | 1   | 2     | 3   | 4   | 5   | 6   | 7   |
|-----|-----|-------|-----|-----|-----|-----|-----|
| `0` | `0` | Start | `0` | U/D | R/L | U/D | R/L |

#### Butttons

| 0   | 1   | 2   | 3 | 4 | 5 | 6   | 7 |
|-----|-----|-----|---|---|---|-----|---|
| `0` | `0` | `0` | C | A | X | `0` | B |
