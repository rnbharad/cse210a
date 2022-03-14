You can utilize "make" to create a while-ss file.

Then, we utilize "bash test.sh" to run the test cases.

Ignore the while-ss error, it does not affect any other portion of the project. I was not able
to create an executable. But, my code does in fact work perfectly, and all my test cases
execute perfectly.

Here is my previous comments on my HW2:
I originally tried to base my entire WHILE interpreter from my ARITH interpreter, using the same formatting and technique as previously. This was giving me many bugs that seemed to have no easy solution, and were technical
so I decided to scrap this approach and try elsewhere. I then tried to utilize the YACC library, as mentioned by some of my peers, but I was not able to get this running. I then tried to utilize the LARK library,
as I read online that this was super easy for parsing and interpreting as opposed to other techniques. I could not solve an issue with my computer where the LARK-parser library would load properly on Python. I was working without any 
resources besides the documentation of these documents, but was not able to get anything running. This is why this assignment is almost 5 weeks late. At the end, I revisited some techniques/resources/implementations from online, 
and implemented the one that was most similar to my ARITH implementation.

Here is my comments on my HW4:
Once again, I was not able to get my code up and running for HW4, since I was trying to continue my HW2 implementation from scratch, rather using a different a different resource. I ended up continuing to use the resource from online, and
implemented it properly. I was able to get all my test cases working except for 1, which I believe is an error that I had. I had moved from my school computer to my home computer, so had a lot of errors getting UBUNTU set back up and
downloading the packages etc to run the files on my computer. That is another reason it took a long time.  


I utilized the cited sources to develop my parser and interpreter. There were parts not referenced in these resources that I had to implement myself.

Cited Sources:
https://ruslanspivak.com/lsbasi-part7/
https://ruslanspivak.com/lsbasi-part8/
https://ruslanspivak.com/lsbasi-part9/
https://github.com/alexsalman

The TA gave advice on how to create the make file and run the program on Windows vs UNIX.
I utilized this information to fit my needs on how to run the test cases.

My own 5 created test cases are in the hard.bats file.

