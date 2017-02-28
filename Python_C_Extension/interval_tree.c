//author: Chunpai Wang

#include <Python.h>
#include "structmember.h"


//node for interval tree
typedef struct{
    PyObject_HEAD
    int low;
    int high;
    int max;
    PyObject *left, *right;
}ITNode;

/*
static PyObject* ITNode_new(PyTypeObject *type, PyObject *args, PyObject *kwds){
    ITNode *self;
    self = (ITNode *)type->tp_alloc(type,0);
    if (self != NULL){
        self->low = 0;
        self->high = 0;
        self->max = 0;
        self->left = NULL;
        self->right = NULL;
    }
    return (PyObject *)self;
}
*/
/*
static int ITNode_init(ITNode *self, PyObject *args, PyObject *kwds){
    //ITNode *left = NULL, *right =NULL, *tmp;
    static char *kwlist[] = {"low","high","max","left","right",NULL};
    if (! PyArg_ParseTupleAndKeywords(args, kwds, "|iiiOO", kwlist,&self->low,&self->high,&self->max,&self->left,&self->right))
        return -1; 
    
    if (left){
        tmp = self->left;
        Py_INCREF(left);
        self->left = left;
        Py_XDECREF(tmp);
    }
    
    if (right){
        tmp = self->right;
        Py_INCREF(right);
        self->right = right;
        Py_XDECREF(tmp);
    }
 
    return 0;
}
*/
static int ITNode_init(ITNode *self, PyObject *args, PyObject *kwds){
    //ITNode *left = NULL, *right =NULL, *tmp;
    static char *kwlist[] = {"low","high","max",NULL};
    if (! PyArg_ParseTupleAndKeywords(args, kwds, "|iii", kwlist,&self->low,&self->high,&self->max))
        return -1;
    return 0;
}
    

static void ITNode_dealloc(ITNode* self){
    Py_XDECREF(self->left);    //need a recursion ??
    Py_XDECREF(self->right);   // need a recursion ?? 
    self->ob_type->tp_free((PyObject*)self);
}


//Each PyMemberDef structure specifies the Python attribute name,
// the C type of the field, the offset into the structure (with the handy offsetof macro), 
// some flags, and a docstring for the attribute. 
// The array will be used later in the type definition.
// this part allow directly access attribute in python interpreter, like   ITNode.low
static PyMemberDef ITNode_members[] = {
    {"low", T_INT, offsetof(ITNode, low), 0, "lower bound of interval"},
    {"high", T_INT, offsetof(ITNode, high), 0, "higher bound of interval"},
    {"max", T_INT, offsetof(ITNode, max), 0, "max of subtree"},
    {"left", T_OBJECT, offsetof(ITNode, left), 0, "left child"},
    {"right", T_OBJECT, offsetof(ITNode, right), 0, "right child"},
    {NULL}
};



/************************************************************************************/

static PyTypeObject ITNodeType = {
   PyObject_HEAD_INIT(NULL)
   0,                         /* ob_size */
   "ITNode.ITNode",               /* tp_name */
   sizeof(ITNode),            /* tp_basicsize */
   0,                         /* tp_itemsize */
   (destructor)ITNode_dealloc, /* tp_dealloc */
   0,                         /* tp_print */
   0,                         /* tp_getattr */
   0,                         /* tp_setattr */
   0,                         /* tp_compare */
   0,                         /* tp_repr */
   0,                         /* tp_as_number */
   0,                         /* tp_as_sequence */
   0,                         /* tp_as_mapping */
   0,                         /* tp_hash */
   0,                         /* tp_call */
   0,                         /* tp_str */
   0,                         /* tp_getattro */
   0,                         /* tp_setattro */
   0,                         /* tp_as_buffer */
   Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags*/
   "ITNode object",           /* tp_doc */
   0,                         /* tp_traverse */
   0,                         /* tp_clear */
   0,                         /* tp_richcompare */
   0,                         /* tp_weaklistoffset */
   0,                         /* tp_iter */
   0,                         /* tp_iternext */
   0,                         /* tp_methods */
   ITNode_members,            /* tp_members */
   0,                         /* tp_getset */
   0,                         /* tp_base */
   0,                         /* tp_dict */
   0,                         /* tp_descr_get */
   0,                         /* tp_descr_set */
   0,                         /* tp_dictoffset */
   (initproc)ITNode_init,     /* tp_init */
   0,                         /* tp_alloc */
   0,                         /* tp_new */
};

//insert c function
void insert(ITNode *root, ITNode *newNode){
    if (newNode->low < root->low){
        if (root->left != NULL)
            insert(root->left, newNode);
        else
            root->left = newNode;
            Py_INCREF(root->left);
            //Py_XDECREF(newNode);         
    }
    else{
        if (root->right != NULL)
            insert(root->right, newNode);
        else
            root->right = newNode;
            Py_INCREF(root->right);
            //Py_XDECREF(newNode);
    }
    if (root->max < newNode->high)
        root->max = newNode->high;
}

// wrap for insert function
static PyObject* wrap_insert(PyObject *self, PyObject *args){
    ITNode *root;
    ITNode *newNode;
    if (!PyArg_ParseTuple(args, "OO", &root,&newNode))
        return NULL;
    /*
    if(root && newNode){
        Py_INCREF(root);
        Py_INCREF(newNode);
    }
    */
    insert(root,newNode);
    return Py_BuildValue("i",1);
}


// I was trying to write a insert without wrapper, but failed at recursion.
/*
static PyObject* insert(PyObject *self,PyObject *args){
    ITNode *root;
    //Py_INCREF(root);

    ITNode *newNode;
    //Py_INCREF(newNode);
    if (!PyArg_ParseTuple(args, "OO", &root,&newNode)){
        return NULL;
    }
    
    if(root && newNode){
        Py_INCREF(root);
        Py_INCREF(newNode);
    }
    
    printf("1 root is %p \n",&root);
    
    if (root == NULL){
        return newNode;
    }
    if (newNode->low < root->low){
        if (root->left != NULL){
            //root->left = insert(root->left, newNode);
            insert(root->left, newNode);
        }
        else{
            root->left = newNode;
            Py_INCREF(root->left);
        }
    }
    else{
        if (root->right != NULL){
            //root->right = insert(root->right, newNode);
            printf("3 root right is %p \n",&root->right);
            printf("b is %p \n",&newNode);
            insert(root->right, newNode);
            printf("4 root right is %p \n",&root->right);
        }
        else{
            root->right = newNode;
            Py_INCREF(root->right);
            printf("2 root right address %p \n",root->right);
            printf("a address %p \n",newNode);
            //printf("new node address %p",newNode);
        }
    }
    if (root->max < newNode->high){
        root->max = newNode->high;
    }
    //printf("newNode address %p",newNode);
    //PyObject_Type((PyObject *)root);
    return Py_BuildValue("i",1);
}

static PyObject* doOverlap(PyObject *self, PyObject *args){
    ITNode *node1;
    ITNode *node2;
    if (!PyArg_ParseTuple(args, "OO", &node1,&node2)){
        return Py_BuildValue("s","Not Valid Parameters");
    }
    printf("%d %d %d %d",node1->low,node2->high,node2->low,node1->high);
    if((node1->low <=  node2->high) && (node2->low <= node1->high)){
        //printf("%s","hahahahahahha");
        return Py_BuildValue("i",1);
    }
    return Py_BuildValue("i",0);
}
*/

//doOverlap function: check if two node overlap
int doOverlap(ITNode *node1, ITNode *node2){
    if(node1->low <= node2->high && node2->low <= node1->high)
        return 1;
    return 0;
}

// search the node in the tree which overlap with searchNode
ITNode* overlapSearch(ITNode *root, ITNode *searchNode){
    if (doOverlap(root,searchNode))
        return root;
    if (root->left != NULL)
        return overlapSearch(root->left, searchNode);
    else if (root->right != NULL)
        return overlapSearch(root->right, searchNode);
    else
        return NULL;
}

//wrap for overlapSearch function
static PyObject* wrap_overlapSearch(PyObject* self, PyObject *args){
    ITNode *root;
    ITNode *searchNode;
    if (!PyArg_ParseTuple(args, "OO", &root,&searchNode))
        return NULL;
    overlapSearch(root, searchNode);
    //Py_INCREF(result);
    return Py_BuildValue("i",1);
}


static PyMethodDef intervalTreeMethods[] = {
    {"insert", (PyCFunction)wrap_insert, METH_VARARGS, "insert interval"},
    //{"doOverlap",(PyCFunction)doOverlap, METH_VARARGS, "check given two intervals if overlap"},
    {"overlapSearch",(PyCFunction)wrap_overlapSearch, METH_VARARGS, "overlap search"},
    {NULL}
};

void initintervalTree(void){
   PyObject* mod;
   // Create the module
   mod = Py_InitModule3("intervalTree", intervalTreeMethods, "An extension with a interval tree.");
   if (mod == NULL) {
      return;
   }
   // Fill in some slots in the type, and make it ready
   ITNodeType.tp_new = PyType_GenericNew;
   if (PyType_Ready(&ITNodeType) < 0) {
      return;
   }
   // Add the type to the module.
   Py_INCREF(&ITNodeType);
   PyModule_AddObject(mod, "ITNode", (PyObject*)&ITNodeType);
}






/**************************************scrap*******************************/

/*
static PyObject* ITNode_insert(ITNode *self, ITNode * new_node){
    if (self == NULL){
        return new_node;
    }
    if (new_node->low < self->low){
        self->left = ITNode_insert(self->left, new_node);
    }
    else{
        self->right = ITNode_insert(self->right, new_node);     
    }
    if (self->max < new_node->high){
        self->max = new_node->high;
    }
    //printf("%s",root->max);
    //printf("%d",new_node->max);
    return self;
}


static PyMethodDef ITNode_methods[] = {
   {"insert",(PyCFunction) ITNode_insert, METH_VARARGS,"insert interval"},
   {NULL}
};
*/


/*
// struct Interval
typedef struct{
    PyObject_HEAD    //This is a macro that creates the initial fields in the structure. This is what makes structure usable as a PyObject.
    int low;
    int high;
}Interval;

//initialization
static int Interval_init(Interval *self, PyObject *args, PyObject *kwds){
    self->low = 0;
    self->high = 0;
    return 0
}

static void Interval_dealloc(Interval* self){
    self->ob_type->tp_free((PyObject*) self);
}
*/

/*
static PyObject* ITNode_set(ITNode *self, PyObject *args){
    int low,high,max;
    PyObject *left, *right;
    if (!PyArg_ParseTuple(args,"iiiOO", &self->low,&self->high,&self->max,&self->left,&self->right)){
        return NULL;
    }
    return Py_BuildValue("i",self->max);
}
*/

//We dont need this anymore, because we have member funcitons
/**********************************setter and getter Methods***********************************/
/*
static  PyObject* ITNode_getlow(ITNode *self){
    return Py_BuildValue("i",self->low);
}

static PyObject* ITNode_setlow(ITNode *self, PyObject *args){
    if (!PyArg_ParseTuple(args, "i", &self->low)) {
          return NULL;
    }
    return Py_BuildValue("i",self->low);
}

static PyObject* ITNode_gethigh(ITNode *self){
    return Py_BuildValue("i",self->high);
}

static PyObject* ITNode_sethigh(ITNode *self, PyObject *args){
    if (!PyArg_ParseTuple(args, "i", &self->high)){
        return NULL;
    }
    return Py_BuildValue("i",self->high);
}

static PyObject* ITNode_getmax(ITNode *self){
    return Py_BuildValue("i",self->max);
}

static PyObject* ITNode_setmax(ITNode *self, PyObject *args){
    if (!PyArg_ParseTuple(args, "i", &self->max)){
        return NULL;
    }
    return Py_BuildValue("i",self->max);
}

static PyMethodDef ITNode_methods[] = {
    {"getlow",(PyCFunction) ITNode_getlow, METH_NOARGS, "get the low value of the interval node"},
    {"setlow",(PyCFunction) ITNode_setlow, METH_VARARGS, "set the low value"},
    {"gethigh",(PyCFunction) ITNode_gethigh, METH_NOARGS, "get the high value of the interval node"},
    {"sethigh",(PyCFunction) ITNode_sethigh, METH_VARARGS, "set the high value"},
    {"getmax",(PyCFunction) ITNode_getmax, METH_NOARGS, "get the max value of the interval node"},
    {"setmax",(PyCFunction) ITNode_setmax, METH_VARARGS, "set the max value"},
    {NULL}
};
*/


/*
static PyGetSetDef ITNode_getseters[] = {
    {"low",(getter)ITNode_getlow,(setter)ITNode_setlow,"low",NULL},
    {"high",(getter)ITNode_gethigh,(setter)ITNode_sethigh,"high",NULL},
    {"max",(getter)ITNode_getmax,(setter)ITNode_setmax,"max",NULL},
    {NULL}
};
*/

/*
static PyObject* py_interval_tree(PyObject* self)
{
    return Py_BuildValue("s", "Hello, Python extensions!!");
}

static PyObject* add_interval(PyObject* self)



static char py_interval_tree_docs[] =
    "py_interval_tree( ): Any message you want to put here!!\n";

static PyMethodDef py_interval_tree_funcs[] = {
    {"py_interval_tree", (PyCFunction)py_interval_tree, METH_NOARGS, helloworld_docs},
    {NULL}
};

void inithelloworld(void)
{
    Py_InitModule3("helloworld", helloworld_funcs,
                   "Extension module example!");
}
*/















