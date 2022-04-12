% Zadání č. 39:
% Napište program řešící úkol daný predikátem u39(LIN,VIN1,VIN2,VOUT), 
% kde LIN je vstupní číselný seznam a VIN1 a VIN2 jsou vstupní proměnné 
% obsahující přirozená čísla splňující podmínku VIN1>VIN2. Proměnná VOUT 
% je výstupní proměnná, ve které se vrací maximální číslo ze seznamu LIN 
% splňující podmínku VIN1>VOUT>VIN2, jinak se v proměnné VOUT vrací nula.

% Testovací predikáty:                       		% VOUT 
u39_1:- u39([4,-3,1,8,3,8,21],12,2,VOUT),write(VOUT).	% 8
u39_2:- u39([4.56],12,2,VOUT),write(VOUT).		% 4.56
u39_3:- u39([],12,2,VOUT),write(VOUT).			% 0
u39_4:- u39([2,-5,0,26,14,3,-1],12,1,VOUT),write(VOUT).
u39_r:- write('Zadej LIN: '),read(LIN),
	write('Zadej VIN1: '),read(VIN1),
	write('Zadej VIN2: '),read(VIN2),
	u39(LIN,VIN1,VIN2,VOUT),write(VOUT).
u39(LIN,VIN1,VIN2,VOUT):- maxlist(LIN,VOUT,VIN1,VIN2),!.
maxlist([X,Y|Z],M,MAX,MIN):- maxlist([Y|Z],Mrest,MAX,MIN),max(X,Mrest,M,MAX,MIN).
maxlist([X],Z,MAX,MIN):- MAX>X,MIN<X,Z is X;Z is 0.
maxlist([],0,MAX,MIN). 
max(X,Y,X,MAX,MIN):- X>=Y,MAX>X,MIN<X.
max(X,Y,Y,MAX,MIN).