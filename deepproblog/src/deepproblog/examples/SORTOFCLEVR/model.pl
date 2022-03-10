% We know that there are two objects in a four grid space. Two shapes possible, two colors possible.
% The green cnn detects the position, and the shape --> x. If x < size: Shape = rectangle. Else: shape = circle. (x modulo size = position)  

width(6).
size(N) :-
    width(Width),
    N is Width * Width.
states(N) :-
    size(Size),
    N is Size * 2.

% [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
% [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
% [0, 1, 2, 3, 4, 5, 6, 7]
nn(cnn_red,[X],Y_red, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(red, X, Y_red).
nn(cnn_green,[X], Y_green, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(green, X, Y_green).
nn(cnn_blue,[X],Y_blue, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(blue, X, Y_blue).
nn(cnn_orange,[X], Y_orange, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(orange, X, Y_orange).

detect_same_states(Shape, Img, Count) :-
    check_state(red, Shape, Img, Return_red),
    check_state(green, Shape, Img, Return_green),
    check_state(blue, Shape, Img, Return_blue),
    check_state(orange, Shape, Img, Return_orange),
    check_state(grey, Shape, Img, Return_grey),
    check_state(yellow, Shape, Img, Return_yellow),
    Count is Return_red + Return_green + Return_blue + Return_orange + Return_grey + Return_yellow.

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

grey_shape(Img, Rectangle) :-
    shape_is_rectangle(Img, grey),
    Rectangle = 1.
grey_shape(Img, Rectangle) :-
    \+ shape_is_rectangle(Img, grey),
    Rectangle = 0.

yellow_shape(Img, Rectangle) :-
    shape_is_rectangle(Img, yellow),
    Rectangle = 1.
yellow_shape(Img, Rectangle) :-
    \+ shape_is_rectangle(Img, yellow),
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

grey_horizontal_side(Img, Left) :-
    position_is_left(Img, grey),
    Left = 1.
grey_horizontal_side(Img, Left) :-
    \+ position_is_left(Img, grey),
    Left = 0.

yellow_horizontal_side(Img, Left) :-
    position_is_left(Img, yellow),
    Left = 1.
yellow_horizontal_side(Img, Left) :-
    \+ position_is_left(Img, yellow),
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

grey_vertical_side(Img, Bottom) :-
    position_is_bottom(Img, grey),
    Bottom = 1.
grey_vertical_side(Img, Bottom) :-
    \+ position_is_bottom(Img, grey),
    Bottom = 0.

yellow_vertical_side(Img, Bottom) :-
    position_is_bottom(Img, yellow),
    Bottom = 1.
yellow_vertical_side(Img, Bottom) :-
    \+ position_is_bottom(Img, yellow),
    Bottom = 0.

position_is_bottom(Img, Color) :-
    detect_state(Color, Img, Y_color),
    position(Y_color, Pos),
    bottom_side(Pos).


% BINARY QUESTION
% Question about the number of same shapes like that one
red_number_of_shapes(Img, Count) :-
    detect_state(red, Img, Y_red),
    to_shape(Y_red, Shape),
    detect_same_states(Shape, Img, Count).
green_number_of_shapes(Img, Count) :-
    detect_state(green, Img, Y_green),
    to_shape(Y_green, Shape),
    detect_same_states(Shape, Img, Count).
blue_number_of_shapes(Img, Count) :-
    detect_state(blue, Img, Y_blue),
    to_shape(Y_blue, Shape),
    detect_same_states(Shape, Img, Count).
orange_number_of_shapes(Img, Count) :-
    detect_state(orange, Img, Y_orange),
    to_shape(Y_orange, Shape),
    detect_same_states(Shape, Img, Count).
grey_number_of_shapes(Img, Count) :-
    detect_state(grey, Img, Y_grey),
    to_shape(Y_grey, Shape),
    detect_same_states(Shape, Img, Count).
yellow_number_of_shapes(Img, Count) :-
    detect_state(yellow, Img, Y_yellow),
    to_shape(Y_yellow, Shape),    
    detect_same_states(Shape, Img, Count).

to_shape(Y_color, Shape) :-
    size(Size),
    Y_color < Size,
    Shape = 0. % Shape = 0 --> Rectangle 
to_shape(Y_color, Shape) :-
    size(Size),
    Y_color >= Size,
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