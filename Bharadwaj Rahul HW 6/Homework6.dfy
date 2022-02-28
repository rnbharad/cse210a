datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)
// need to do cases for both arguments of input (for Tree, Node and Leaf).. leaf goes to Nil
function flatten<T>(tree:Tree<T>):List<T>
{
	    match tree
    case Leaf => Nil
    case Node(Tree1, Tree2, T1) => append(Cons(T1, flatten(Tree1)), flatten(Tree2))
}

function append<T>(xs:List<T>, ys:List<T>):List<T> //TAKEN FROM CLASS NOTES
ensures xs == Nil ==> append(xs, ys) == ys
ensures ys == Nil ==> append(xs, ys) == xs
//append(xs, ys) if xs is Nil, ys
//append(xs, ys) if ys is Nil, xs
{
        match xs
    case Nil => ys
    case Cons(x, xs') => Cons(x, append(xs',ys))
}

function treeContains<T>(tree:Tree<T>, element:T):bool
{
        match tree
    case Leaf => false
    case Node(Tree1, Tree2, T1) => element==T1 || treeContains(Tree1, element) || treeContains(Tree2, element)
    //case Cons(0, xs) => Cons(element, xs)
}

function listContains<T>(xs:List<T>, element:T):bool
{
        match xs
    case Nil => false
    case Cons(element1, xs') => element==element1 || listContains(xs', element)
    //case Cons(0, xs) => Cons(element, xs)
}

lemma memberOfAppend<T>(x:T, ys:List<T>, zs:List<T>) //TAKEN FROM CLASS NOTES
ensures listContains(append(ys,zs), x) == (listContains(ys,x) || listContains(zs,x))
{
        match ys
    case Nil => {}
    case Cons(y, ys') => memberOfAppend(x,ys',zs);
    //i scrapped out the assert statements, since we don't really need them, and it's something i got from the class notes
}    

lemma sameElements<T>(tree:Tree<T>, element:T)
ensures treeContains(tree, element) <==> listContains(flatten(tree), element)
{
    match tree
    case Leaf => {}
    case Node(Tree1, Tree2, T1) => {
        memberOfAppend(element, flatten(Tree1), flatten(Tree2));
        sameElements(Tree1, element);
        sameElements(Tree2, element);

        assert treeContains(tree, element)
            == treeContains(Node(Tree1, Tree2, T1), element) //using definition of tree

            == treeContains(Tree1, element) || treeContains(Tree2, element) || element==T1 //using treeContains func

            == element==T1 || listContains(flatten(Tree1), element) || listContains(flatten(Tree2), element) //using inductive hypothesis

            == listContains(append(flatten(Tree1), flatten(Tree2)), element) //using memberOfAppend method

            == listContains(Cons(T1, append(flatten(Tree1), flatten(Tree2))), element) //using listContains func

            == listContains(Cons(T1, flatten(tree)), element)

            == listContains(flatten(tree), element);
    }
}
        /* wrong code
        assert listContains(flatten(tree), element)
            == listContains(flatten(Node(Tree1, Tree2, T1)), element) //using Tree definition
            == listContains((append(Cons(T1, flatten(Tree1)), flatten(Tree2))), element) //definition of flatten
            == listContains(Cons(T1, flatten(Tree1)), element) || listContains(flatten(Tree2), element) //using memberOfAppend
            == listContains(flatten(Tree1), element) || listContains(flatten(Tree2), element) //using definition of List
            == treeContains(Tree1, element) || treeContains(Tree2, element) //using inductive hypothesis
            == treeContains(tree, element);
        */  
        