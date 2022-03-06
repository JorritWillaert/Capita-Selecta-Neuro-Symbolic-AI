% We know that there are two objects in a four grid space. Two shapes possible, two colors possible.
% The green cnn detects the position, and the shape --> x. If x < 4: Shape = rectangle. Else: shape = circle. (x modulo 4 = position)  

nn(cnn_red,[X],Y,[0,1,2,3,4,5,6,7]) :: detect_green_state(X,Y_red).
nn(cnn_green, [X], Y, [0,1,2,3,4,5,6,7]) :: detect_red_state(X, Y_green).

shape_is_rectangle(Out) :-
    Out < 4.

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