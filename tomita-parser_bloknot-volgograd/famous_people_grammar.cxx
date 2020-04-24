#encoding "utf8"

// Различный порядок имени, фамилии и отчества
FullFIO_1 -> Word<h-reg1, gram="имя", fio-agr[1]> Word<h-reg1, gram="отч", fio-agr[1]> Word<h-reg1, gram="фам", fio-agr[1]>;
FullFIO_2 -> Word<h-reg1, gram="имя", fio-agr[1]> Word<h-reg1, gram="фам", fio-agr[1]> Word<h-reg1, gram="отч", fio-agr[1]>;
FullFIO_3 -> Word<h-reg1, gram="отч", fio-agr[1]> Word<h-reg1, gram="имя", fio-agr[1]> Word<h-reg1, gram="фам", fio-agr[1]>;
FullFIO_4 -> Word<h-reg1, gram="отч", fio-agr[1]> Word<h-reg1, gram="фам", fio-agr[1]> Word<h-reg1, gram="имя", fio-agr[1]>;
FullFIO_5 -> Word<h-reg1, gram="фам", fio-agr[1]> Word<h-reg1, gram="имя", fio-agr[1]> Word<h-reg1, gram="отч", fio-agr[1]>;
FullFIO_6 -> Word<h-reg1, gram="фам", fio-agr[1]> Word<h-reg1, gram="отч", fio-agr[1]> Word<h-reg1, gram="имя", fio-agr[1]>;
FullFIO -> FullFIO_1 | FullFIO_2 | FullFIO_3 | FullFIO_4 | FullFIO_5 | FullFIO_6;

// Одна буква инициалов - пример: А.
ShortInitial -> Word<wff=/[А-Я]\./>;

// Две буквы инициалов - пример: А. С.
FullInitial -> ShortInitial ShortInitial;

Initial -> ShortInitial | FullInitial;

// Инициал с двумя полными частятим имени, например: Л. Владимир Ильич
InitialWithFIO_1 -> ShortInitial Word<h-reg1, gram="имя"> Word<h-reg1, gram="отч">;
InitialWithFIO_2 -> ShortInitial Word<h-reg1, gram="имя"> Word<h-reg1, gram="фам">;
InitialWithFIO_3 -> ShortInitial Word<h-reg1, gram="фам"> Word<h-reg1, gram="имя">;
InitialWithFIO_4 -> ShortInitial Word<h-reg1, gram="фам"> Word<h-reg1, gram="отч">;
InitialWithFIO_5 -> ShortInitial Word<h-reg1, gram="отч"> Word<h-reg1, gram="имя">;
InitialWithFIO_6 -> ShortInitial Word<h-reg1, gram="отч"> Word<h-reg1, gram="фам">;
InitialWithFIO -> InitialWithFIO_1 | InitialWithFIO_2 | InitialWithFIO_3 | InitialWithFIO_4 | InitialWithFIO_5 | InitialWithFIO_6;

// Две полных части имени с инициалом, например: Владимир Ильич Л. 
FIOWithInitial_1 -> Word<h-reg1, gram="имя"> Word<h-reg1, gram="отч"> ShortInitial;
FIOWithInitial_2 -> Word<h-reg1, gram="имя"> Word<h-reg1, gram="фам"> ShortInitial;
FIOWithInitial_3 -> Word<h-reg1, gram="фам"> Word<h-reg1, gram="имя"> ShortInitial;
FIOWithInitial_4 -> Word<h-reg1, gram="фам"> Word<h-reg1, gram="отч"> ShortInitial;
FIOWithInitial_5 -> Word<h-reg1, gram="отч"> Word<h-reg1, gram="имя"> ShortInitial;
FIOWithInitial_6 -> Word<h-reg1, gram="отч"> Word<h-reg1, gram="фам"> ShortInitial;
FIOWithInitial -> FIOWithInitial_1 | FIOWithInitial_2 | FIOWithInitial_3 | FIOWithInitial_4 | FIOWithInitial_5 | FIOWithInitial_6;

// Инициалы с одной частью имени, например: В. И. Ленин
InitialsWithFIO_1 -> Initial Word<h-reg1, gram="имя">;
InitialsWithFIO_2 -> Initial Word<h-reg1, gram="отч">;
InitialsWithFIO_3 -> Initial Word<h-reg1, gram="фам">;
InitialsWithFIO -> InitialsWithFIO_1 | InitialsWithFIO_2 | InitialsWithFIO_3;

// Одна часть имени с инициалами, например: Ленин В. И.
FIOWithInitials_1 -> Word<h-reg1, gram="имя"> Initial;
FIOWithInitials_2 -> Word<h-reg1, gram="отч"> Initial;
FIOWithInitials_3 -> Word<h-reg1, gram="фам"> Initial;
FIOWithInitials -> FIOWithInitials_1 | FIOWithInitials_2 | FIOWithInitials_3;

// Две части имени, например: Владимир Ильич
FI_1 -> Word<h-reg1, gram="имя", fio-agr[1]> Word<h-reg1, gram="отч", fio-agr[1]>;
FI_2 -> Word<h-reg1, gram="отч", fio-agr[1]> Word<h-reg1, gram="имя", fio-agr[1]>;
FI_3 -> Word<h-reg1, gram="имя", fio-agr[1]> Word<h-reg1, gram="фам", fio-agr[1]>;
FI_4 -> Word<h-reg1, gram="фам", fio-agr[1]> Word<h-reg1, gram="имя", fio-agr[1]>;
FI_5 -> Word<h-reg1, gram="фам", fio-agr[1]> Word<h-reg1, gram="отч", fio-agr[1]>;
FI_6 -> Word<h-reg1, gram="отч", fio-agr[1]> Word<h-reg1, gram="фам", fio-agr[1]>;
FI -> FI_1 | FI_2 |FI_3 |FI_4 |FI_5 |FI_6;

FIO -> FullFIO | InitialWithFIO | FIOWithInitial | InitialsWithFIO | FIOWithInitials | FI;

//FamousDesignator -> "знаменитый" | "уважаемый" | "заслуженный";

PersonName -> FIO interp(PersonFact.Name);




