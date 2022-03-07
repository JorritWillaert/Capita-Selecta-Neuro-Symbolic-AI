% We know that there are two objects in a four grid space. Two shapes possible, two colors possible.
% The green cnn detects the position, and the shape --> x. If x < 4: Shape = rectangle. Else: shape = circle. (x modulo 4 = position)  

nn(cnn_red,[X],Y_red,[0,1,2,3,4,5,6,7]) :: detect_state(red, X, Y_red).
nn(cnn_green, [X], Y_green, [0,1,2,3,4,5,6,7]) :: detect_state(green, X, Y_green).

shape(red, Img, rectangle) :-
    detect_state(red, Img, Y_red),
    Y_red < 4.

shape(green, Img, rectangle) :-
    detect_state(green, Img, Y_green),
    Y_green < 4.

horizontal_side(red, Img, left) :-
    detect_state(red, Img, Y_red),
    position(Y_red, Pos),
    left_side(Pos).

horizontal_side(green, Img, left) :-
    detect_state(green, Img, Y_green),
    position(Y_green, Pos),
    left_side(Pos).

vertical_side(red, Img, bottom) :-
    detect_state(red, Img, Y_red),
    position(Y_red, Pos),
    bottom_side(Pos).

vertical_side(green, Img, bottom) :-
    detect_state(green, Img, Y_green),
    position(Y_green, Pos),
    bottom_side(Pos).

position(Out, Pos) :-
    Pos is Out mod 4.

left_side(Out) :-
    to_coor(Out, X, Y),
    X < 1.

bottom_side(Out) :-
    to_coor(Out, X, Y),
    Y >= 1. % Be careful. Y axis runs down!

to_coor(Out, X, Y) :-
    X is Out mod 2, 
    Y is Out // 2.