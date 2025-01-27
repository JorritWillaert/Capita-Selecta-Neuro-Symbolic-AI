% Grid = 6 by 6

width(6).
size(N) :-
    width(Width),
    N is Width * Width.
states(N) :-
    size(Size),
    N is Size * 2.

nn(cnn_red,[X],Y_red, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(red, X, Y_red).
nn(cnn_green,[X], Y_green, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(green, X, Y_green).
nn(cnn_blue,[X],Y_blue, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(blue, X, Y_blue).
nn(cnn_orange,[X], Y_orange, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(orange, X, Y_orange).
nn(cnn_grey,[X], Y_grey, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(grey, X, Y_grey).
nn(cnn_yellow,[X], Y_yellow, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]) :: detect_state(yellow, X, Y_yellow).

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
shape(Img, Color, Rectangle) :-
    shape_is_rectangle(Img, Color),
    Rectangle = 1.
shape(Img, Color, Rectangle) :-
    \+ shape_is_rectangle(Img, Color),
    Rectangle = 0.

shape_is_rectangle(Img, Color) :-
    detect_state(Color, Img, Y_color),
    size(Size),
    Y_color < Size.

% Question about the horizontal side
horizontal_side(Img, Color, Left) :-
    position_is_left(Img, Color),
    Left = 1.
horizontal_side(Img, Color, Left) :-
    \+ position_is_left(Img, Color),
    Left = 0.

position_is_left(Img, Color) :-
    detect_state(Color, Img, Y_color),
    position(Y_color, Pos),
    left_side(Pos).

% Question about the vertical side
vertical_side(Img, Color, Bottom) :-
    position_is_bottom(Img, Color),
    Bottom = 1.
vertical_side(Img, Color, Bottom) :-
    \+ position_is_bottom(Img, Color),
    Bottom = 0.

position_is_bottom(Img, Color) :-
    detect_state(Color, Img, Y_color),
    position(Y_color, Pos),
    bottom_side(Pos).


% BINARY QUESTION
% Question about the number of same shapes like that one
number_of_shapes(Img, Color, Count) :-
    detect_state(Color, Img, Y_red),
    to_shape(Y_red, Shape),
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