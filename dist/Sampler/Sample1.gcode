;###loadtip
G28
G0 Z10
G0 X146.5 Y5 F2000
G0 Z1.5 F1250
G0 Z32 F1500
;###sample
G0 X9.5 Y4.5 F2000
G0 Z5 F1500
M400
M42 P45 S255
G4 S3
M42 P39 S255
G4 P1
M42 P39 S0
M42 P45 S0
G0 Z20 F1500
G0 X9.5 Y49.5 F2000
G0 Z5 F1500
M400
M42 P43 S255
G4 S3
M42 P41 S255
G4 P3
M42 P41 S0
M42 P43 S0
;###eject tip
G0 Z30 F1000
G0 X110 Y70 F3000
G0 X190 F2000
M18 X Y
G0 Z37 F1500
G0 X110 F2000
G28
M18
;###loadtip
G28
G0 Z10
G0 X146.5 Y11.7 F2000
G0 Z1.5 F1250
G0 Z32 F1500
;###sample
G0 X9.5 Y13.5 F2000
G0 Z5 F1500
M400
M42 P45 S255
G4 S3
M42 P39 S255
G4 P1
M42 P39 S0
M42 P45 S0
G0 Z20 F1500
G0 X9.5 Y58.5 F2000
G0 Z5 F1500
M400
M42 P43 S255
G4 S3
M42 P41 S255
G4 P3
M42 P41 S0
M42 P43 S0
;###eject tip
G0 Z30 F1000
G0 X110 Y70 F3000
G0 X190 F2000
M18 X Y
G0 Z37 F1500
G0 X110 F2000
G28
M18
;###loadtip
G28
G0 Z10
G0 X146.5 Y18.7 F2000
G0 Z1.5 F1250
G0 Z32 F1500
;###sample
G0 X9.5 Y22.5 F2000
G0 Z5 F1500
M400
M42 P45 S255
G4 S3
M42 P39 S255
G4 P1
M42 P39 S0
M42 P45 S0
G0 Z20 F1500
G0 X9.5 Y67.5 F2000
G0 Z5 F1500
M400
M42 P43 S255
G4 S3
M42 P41 S255
G4 P3
M42 P41 S0
M42 P43 S0
;###eject tip
G0 Z30 F1000
G0 X110 Y70 F3000
G0 X190 F2000
M18 X Y
G0 Z37 F1500
G0 X110 F2000
G28
M18
