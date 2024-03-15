fun str_to_int_list s = List.filter (fn c => c <> 10)
  (List.map Char.ord (String.explode s));

fun shift k l = List.map (fn i => i + k) l;

fun rotate k l: int list = 
  case l of
       [] => []
     | c => let
       val dist = (List.length c) - (k mod (List.length c))
            in
              List.drop (c, dist) @ List.take (c, dist)
            end;

fun swap (a::b::r) = b::a::(swap r)
  | swap (a::[]) = [a]
  | swap [] = [];

val flag = [105, 115, 132, 105, 85, 162, 102, 142, 90, 138, 155, 121, 144, 160,
104, 114, 107, 122, 86, 89, 114, 113, 121, 132, 103, 89, 88, 88, 113, 102, 114, 114];

val encrypt = (shift 50) o (rotate 3) o swap o (rotate 5) o swap o (shift ~13);

print "Enter flag: ";
val user_input = valOf (TextIO.inputLine TextIO.stdIn);

if (encrypt (str_to_int_list user_input)) = flag
then print "Correct!\n"
else print "Wrong!\n";
