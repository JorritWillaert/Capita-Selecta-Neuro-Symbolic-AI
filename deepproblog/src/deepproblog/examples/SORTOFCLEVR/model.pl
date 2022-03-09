% We know that there are two objects in a four grid space. Two shapes possible, two colors possible.
% The green cnn detects the position, and the shape --> x. If x < 4: Shape = rectangle. Else: shape = circle. (x modulo 4 = position)  

nn(cnn_red,[X],Y_red,[0,1,2,3,4,5,6,7]) :: detect_state(red, X, Y_red).
nn(cnn_green, [X], Y_green, [0,1,2,3,4,5,6,7]) :: detect_state(green, X, Y_green).

red_shape(Img, Rectangle) :-
    detect_state(red, Img, Y_red),
    Y_red < 4,
    Rectangle = 1.
red_shape(Img, Rectangle) :-
    detect_state(red, Img, Y_red),
    Y_red >= 4,
    Rectangle = 0.

green_shape(Img, Rectangle) :-
    detect_state(green, Img, Y_green),
    Y_green < 4, 
    Rectangle = 1.
green_shape(Img, Rectangle) :-
    detect_state(green, Img, Y_green),
    Y_green >= 4, 
    Rectangle = 0.

red_horizontal_side(Img, Left) :-
    detect_state(red, Img, Y_red),
    position(Y_red, Pos),
    left_side(Pos), 
    Left = 1.
red_horizontal_side(Img, Left) :-
    detect_state(red, Img, Y_red),
    position(Y_red, Pos),
    \+ left_side(Pos), 
    Left = 0.

green_horizontal_side(Img, Left) :-
    detect_state(green, Img, Y_green),
    position(Y_green, Pos),
    left_side(Pos), 
    Left = 1.
green_horizontal_side(Img, Left) :-
    detect_state(green, Img, Y_green),
    position(Y_green, Pos),
    \+ left_side(Pos), 
    Left = 0.

red_vertical_side(Img, Bottom) :-
    detect_state(red, Img, Y_red),
    position(Y_red, Pos),
    bottom_side(Pos), 
    Bottom = 1.
red_vertical_side(Img, Bottom) :-
    detect_state(red, Img, Y_red),
    position(Y_red, Pos),
    \+ bottom_side(Pos), 
    Bottom = 0.

green_vertical_side(Img, Bottom) :-
    detect_state(green, Img, Y_green),
    position(Y_green, Pos),
    bottom_side(Pos), 
    Bottom = 1.
green_vertical_side(Img, Bottom) :-
    detect_state(green, Img, Y_green),
    position(Y_green, Pos),
    \+ bottom_side(Pos), 
    Bottom = 0.

% Note: Do not need red_number_of_shapes and green_number_of_shapes right now. But has been added since this will be necessary later (implementation with same_shape will have to change too though)
red_number_of_shapes(Img, Count) :-
    detect_state(red, Img, Y_red),
    detect_state(green, Img, Y_green),
    same_shape(Y_red, Y_green),
    Count = 2.
red_number_of_shapes(Img, Count) :-
    detect_state(red, Img, Y_red),
    detect_state(green, Img, Y_green),
    \+ same_shape(Y_red, Y_green),
    Count = 1.

green_number_of_shapes(Img, Count) :-
    detect_state(red, Img, Y_red),
    detect_state(green, Img, Y_green),
    same_shape(Y_red, Y_green),
    Count = 2.
green_number_of_shapes(Img, Count) :-
    detect_state(red, Img, Y_red),
    detect_state(green, Img, Y_green),
    \+ same_shape(Y_red, Y_green),
    Count = 1.

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

same_shape(Y1, Y2) :-
    (Y1 >= 4, Y2 >= 4) ; (Y1 < 4, Y2 < 4).