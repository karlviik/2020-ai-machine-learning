cur_year(2019).

man(marcus).
man(jaan).

max_lifespan(mortal, 150).

lives_in(pompej, marcus).
lives_in(pompej, francesco).

all_dead(pompej, 79).

birth(marcus, 40).
birth(jaan, 1977).
birth(francesco, 1989).

mortal(X) :-
	man(X).

naturally_deceased_by(Nimi, Year) :-
	mortal(Nimi), birth(Nimi, Birth), max_lifespan(mortal, Span), (Birth + Span) < Year.

alive_at(Nimi, Year) :-
	birth(Nimi, Birth),
	Year > Birth,
	not(naturally_deceased_by(Nimi, Year)).

killed(Nimi) :-
	lives_in(City, Nimi),
	all_dead(City, Year),
	alive_at(Nimi, Year).

deceased(Nimi) :-
	killed(Nimi), ! ;
	cur_year(Year),	naturally_deceased_by(Nimi, Year).

