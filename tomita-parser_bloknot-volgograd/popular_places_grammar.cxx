#encoding "utf8"

//PopularPlacesDesignator -> 'побывать' | 'посетить' | 'открыть' | 'реставрировать';

// Слова, которые указывают на популярное место
PlacesTypes -> 'музей' | 'музей-панорама' | 'заповедник' | 'памятник' | 'площадь' | 'парк' | 'курган' | 'набережная' | 'храм' | 'аллея' | 'фонтан';

// Название места - одно слово с большой буквы, состоящее только из букв и не стоящее первым в предложении
PlaceName_1 ->  Word<~fw, h-reg1, wff=/[А-Яа-я]+/>;
// Название места - два слова: первое начинается с заглавной буквы
PlaceName_2 ->  AnyWord<~fw, h-reg1, gnc-agr[1], wff=/[А-Яа-я]+/> Word<gnc-agr[1]>;
PlaceName -> PlaceName_1 | PlaceName_2;

// Возле названия достопримечательности должно стоять слово-указатель
//PopularPlaces_1 -> PopularPlacesDesignator<~sp-agr[2]> PlaceName<~sp-agr[2]>;
PopularPlaces_2 -> PlacesTypes PlaceName;
PopularPlaces_3 -> PlaceName PlacesTypes;
PopularPlaces -> PopularPlaces_2 | PopularPlaces_3;

Out -> PopularPlaces interp(PlaceFact.Name);