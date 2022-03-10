% We know that there are two objects in a four grid space. Two shapes possible, two colors possible.
% The green cnn detects the position, and the shape --> x. If x < size: Shape = rectangle. Else: shape = circle. (x modulo size = position)  

width(2).
size(N) :-
    width(Width),
    N is Width * Width.
states(N) :-
    size(Size),
    N is Size * 2.

% [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
% [0, 1, 2, 3, 4, 5, 6, 7]
nn(cnn_red,[X],Y_red, [0, 1, 2, 3, 4, 5, 6, 7]) :: detect_state(red, X, Y_red).
nn(cnn_green, [X], Y_green,  [0, 1, 2, 3, 4, 5, 6, 7]) :: detect_state(green, X, Y_green).
nn(cnn_blue,[X],Y_blue, [0, 1, 2, 3, 4, 5, 6, 7]) :: detect_state(blue, X, Y_blue).
nn(cnn_orange, [X], Y_orange, [0, 1, 2, 3, 4, 5, 6, 7]) :: detect_state(orange, X, Y_orange).

detect_same_states(Shape, Img, Count) :-
    check_state(red, Shape, Img, Return_red),
    check_state(green, Shape, Img, Return_green),
    %check_state(blue, Shape, Img, Return_blue),
    %check_state(orange, Shape, Img, Return_orange),
    %Count is Return_red + Return_green + Return_blue + Return_orange.
    Count is Return_red + Return_green.

check_state(Color, Shape, Img, Return) :-
    detect_state(Color, Img, Y_color),
    to_shape(Y_color, Shape_color),
    Shape =:= Shape_color,
    Return = 1.
check_state(Color, Shape, Img, Return) :-
    detect_state(Color, Img, Y_color),
    to_shape(Y_color, Shape_color),
    Shape =\= Shape_color,
    Return = 0.

% NON-BINARY QUESTIONS
% Question about the shape
red_shape(Img, Rectangle) :-
    shape_is_rectangle(Img, red),
    Rectangle = 1.
red_shape(Img, Rectangle) :-
    \+ shape_is_rectangle(Img, red),
    Rectangle = 0.

green_shape(Img, Rectangle) :-
    shape_is_rectangle(Img, green),
    Rectangle = 1.
green_shape(Img, Rectangle) :-
    \+ shape_is_rectangle(Img, green),
    Rectangle = 0.

blue_shape(Img, Rectangle) :-
    shape_is_rectangle(Img, blue),
    Rectangle = 1.
blue_shape(Img, Rectangle) :-
    \+ shape_is_rectangle(Img, blue),
    Rectangle = 0.

orange_shape(Img, Rectangle) :-
    shape_is_rectangle(Img, orange),
    Rectangle = 1.
orange_shape(Img, Rectangle) :-
    \+ shape_is_rectangle(Img, orange),
    Rectangle = 0.

shape_is_rectangle(Img, Color) :-
    detect_state(Color, Img, Y_color),
    size(Size),
    Y_color < Size.


% Question about the horizontal side
red_horizontal_side(Img, Left) :-
    position_is_left(Img, red),
    Left = 1.
red_horizontal_side(Img, Left) :-
    \+ position_is_left(Img, red),
    Left = 0.

green_horizontal_side(Img, Left) :-
    position_is_left(Img, green),
    Left = 1.
green_horizontal_side(Img, Left) :-
    \+ position_is_left(Img, green),
    Left = 0.

blue_horizontal_side(Img, Left) :-
    position_is_left(Img, blue),
    Left = 1.
blue_horizontal_side(Img, Left) :-
    \+ position_is_left(Img, blue),
    Left = 0.

orange_horizontal_side(Img, Left) :-
    position_is_left(Img, orange),
    Left = 1.
orange_horizontal_side(Img, Left) :-
    \+ position_is_left(Img, orange),
    Left = 0.

position_is_left(Img, Color) :-
    detect_state(Color, Img, Y_color),
    position(Y_color, Pos),
    left_side(Pos).


% Question about the vertical side
red_vertical_side(Img, Bottom) :-
    position_is_bottom(Img, red),
    Bottom = 1.
red_vertical_side(Img, Bottom) :-
    \+ position_is_bottom(Img, red),
    Bottom = 0.

green_vertical_side(Img, Bottom) :-
    position_is_bottom(Img, green),
    Bottom = 1.
green_vertical_side(Img, Bottom) :-
    \+ position_is_bottom(Img, green),
    Bottom = 0.

blue_vertical_side(Img, Bottom) :-
    position_is_bottom(Img, blue),
    Bottom = 1.
blue_vertical_side(Img, Bottom) :-
    \+ position_is_bottom(Img, blue),
    Bottom = 0.

orange_vertical_side(Img, Bottom) :-
    position_is_bottom(Img, orange),
    Bottom = 1.
orange_vertical_side(Img, Bottom) :-
    \+ position_is_bottom(Img, orange),
    Bottom = 0.

position_is_bottom(Img, Color) :-
    detect_state(Color, Img, Y_color),
    position(Y_color, Pos),
    bottom_side(Pos).


% BINARY QUESTION
% Question about the number of same shapes like that one

% Note: Do not need red_number_of_shapes and green_number_of_shapes right now. But has been added since this will be necessary later (implementation with same_shape will have to change too though)
red_number_of_shapes(Img, Count) :-
    detect_state(red, Img, Y_red),
    to_shape(Y_red, Shape),
    detect_same_states(Shape, Img, Count).
green_number_of_shapes(Img, Count) :-
    detect_state(green, Img, Y_green),
    to_shape(Y_green, Shape),
    detect_same_states(Shape, Img, Count).
blue_number_of_shapes(Img, Count) :-
    detect_state(red, Img, Y_blue),
    to_shape(Y_blue, Shape),
    detect_same_states(Shape, Img, Count).
orange_number_of_shapes(Img, Count) :-
    detect_state(orange, Img, Y_orange),
    to_shape(Y_orange, Shape),
    detect_same_states(Shape, Img, Count).

to_shape(Y_color, Shape) :-
    size(Size),
    Y_color < Size,
    Shape = 0. % Shape = 0 --> Rectangle 
to_shape(Y_color, Shape) :-
    size(Size),
    Y_color  >= Size,
    Shape = 1. % Shape = 1 --> Circle


position(Out, Pos) :-
    size(Size),
    Pos is Out mod Size.

left_side(Out) :-
    to_coor(Out, X, Y),
    width(Width),
    X < (Width // 2).

bottom_side(Out) :-
    to_coor(Out, X, Y),
    width(Width),
    Y >= (Width // 2). % Be careful. Y axis runs down!

to_coor(Out, X, Y) :-
    width(Width),
    X is Out mod Width, 
    Y is Out // Width.