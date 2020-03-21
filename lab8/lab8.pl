cur_year(2019).

man(marcus).
man(jaan).

max_lifespan(mortal, 150).

mortal(X) :-
	man(X).

lives_in(pompej, marcus).
lives_in(pompej, francesco).

birth(marcus, 40).
birth(jaan, 1977).
birth(francesco, 1989).


naturally_deceased_by(Nimi, Year) :-
	mortal(Nimi), birth(Nimi, Birth), max_lifespan(mortal, Span), (Birth + Span) < Year.

alive_at(Nimi, Year) :-
	birth(Nimi, Birth),
	Year > Birth,
	not(naturally_deceased_by(Nimi, Year)).

killed(Nimi) :-
	lives_in(pompej, Nimi),
	alive_at(Nimi, 79).

deceased(Nimi) :-
	killed(Nimi), ! ;
	cur_year(Year),	naturally_deceased_by(Nimi, Year).

