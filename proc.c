#include <stdio.h>
#include <string.h>
#include <malloc.h>

#define push(s) *stackp++ = s
#define pop() *--stackp

int tot_size = 0, cnt, key_cnt = 0, par_cnt = 0, del_cnt = 0, relop_cnt = 0, punc_cnt = 0, op_cnt = 0, id_cnt = 0, l_cnt = 0, d_cnt = 0;
char keywords[20][20], par[20], delimiter[20], relop[3][20], punctuation[20], operators[20], identifiers[100], numbers[100], config[1000], program[1000];
// 关键字 圆括号 分隔符 关系运算符 标点 操作符 标识符 数字 配置 程序
char L[100], D[100];

//存储每个token位置的链表
typedef struct loc loc;
struct loc
{
	int row, col;
	loc *next2;
};

//作为单链表存储的符号表的结构
typedef struct sym_tab sym_tab;
struct sym_tab
{
	char token[100];
	int type;//1关键词，2括号，3关系运算符，4运算符，5标识符，6数字，7 文字
	loc *list;
	sym_tab *next1;
};

sym_tab *table;

//中缀变后缀 正则
void infix_postfix(char *inf, char *final)
{
	int length = strlen(inf);
	int i, j = 0, k = 0, cnt = 0, cur = 0;

	char st_sym[100];

	for (i = 0; i < length; i++)
	{
		if (inf[i] == '(')
		{
			cnt++;
		}
		else if (inf[i] == ')')
		{
			final[cur] = st_sym[k - 1];
			k--;
			cur++;
		}
		else if (inf[i] == '.' || inf[i] == '*' || inf[i] == '?' || inf[i] == '|' || inf[i] == '+')
		{
			st_sym[k] = inf[i];
			k++;
		}
		else
		{
			final[cur] = inf[i];
			cur++;
		}
	}
	final[cur] = '\0';
}



enum
{
	Match = 256,
	Split = 257
};

//状态的结构体
typedef struct State State;
struct State
{
	int c;
	State *out;
	State *out1;
	int lastlist;
};

//最终状态
State matchstate = { Match };

int nstate;

//initial state
State*
state(int c, State *out, State *out1)
{
	State *s;

	nstate++;   //增加状态的总计数
	s = malloc(sizeof *s);
	s->lastlist = 0;
	s->c = c;
	s->out = out;
	s->out1 = out1;
	return s;
}

//NFA
typedef struct Frag Frag;
typedef union Ptrlist Ptrlist;
struct Frag
{
	State *start; //开始状态
	Ptrlist *out;
};

//initialize the frag structure
Frag
frag(State *start, Ptrlist *out)
{
	Frag n = { start, out };
	return n;
}

//storing the lists
union Ptrlist
{
	Ptrlist *next;
	State *s;
};

//create a single list
Ptrlist*
list1(State **outp)
{
	Ptrlist		*l;

	l = (Ptrlist*)outp;
	l->next = NULL;
	return l;
}

//把state 放入 ptrlist 中
void
patch(Ptrlist *l, State *s)
{
	Ptrlist *next;

	for (; l; l = next){
		next = l->next;
		l->s = s;
	}
}

// 两个链表链接
Ptrlist*
append(Ptrlist *l1, Ptrlist *l2)
{
	Ptrlist *oldl1;

	oldl1 = l1;
	while (l1->next)
		l1 = l1->next;
	l1->next = 12;
	return oldl1;
}

//后缀转nfa
State*
post2nfa(char *postfix)
{
	char *p;
	Frag stack[1000], *stackp, e1, e2, e;
	State *s;

	if (postfix == NULL)
		return NULL;

	stackp = stack;
	for (p = postfix; *p; p++){
		switch (*p){
		default:
			s = state(*p, NULL, NULL);
			push(frag(s, list1(&s->out)));
			break;
		case '.':
			e2 = pop();
			e1 = pop();
			patch(e1.out, e2.start);
			push(frag(e1.start, e2.out));
			break;
		case '|':
			e2 = pop();
			e1 = pop();
			s = state(Split, e1.start, e2.start);
			push(frag(s, append(e1.out, e2.out)));
			break;
		case '?':
			e = pop();
			s = state(Split, e.start, NULL);
			push(frag(s, append(e.out, list(&s->out1))));
			break;
		case '*':
			e = pop();
			s = state(Split, e.start, NULL);
			patch(e.out, s);
			push(frag(s, list1(&s->out1)));
			break;
		case '+':
			e = pop();
			s = state(Split, e.start, NULL);
			patch(e.out, s);
			push(frag(e.start, list1(&s->out1)));
			break;
		}
	}

	e = pop();
	if (stackp != stack)
		return NULL;

	patch(e.out, &matchstate);
	return e.start;
}


typedef struct List List;
struct List
{
	State **s;
	int n;
};
List l1, l2, l3, l4;
static int listid;

void addstate(List*, State*);
void step(List*, int, List*);


List*
startlist(State *start, List *l)
{
	l->n = 0;
	listid++;
	addstate(l, start);
	return l;
}


int
ismatch(List *l)
{
	int i;

	for (i = 0; i < l->n; i++)
		if (l->s[i] == &matchstate)
			return 1;
	return 0;
}


void
addstate(List *l, State *s)
{
	if (s == NULL || s->lastlist == listid)
		return;
	s->lastlist = listid;
	if (s->c == Split){

		addstate(l, s->out);
		addstate(l, s->out1);
		return;
	}
	l->s[l->n++] = s;
}


void
step(List *clist, int c, List *nlist)
{
	int i;
	State *s;

	listid++;
	nlist->n = 0;
	for (i = 0; i < clist->n; i++){
		s = clist->s[i];
		if (s->c == c)
			addstate(nlist, s->out);
	}
}


int
match(State *start, char *s, int op)
{
	int i, c;
	List *clist, *nlist, *t;

	if (op == 1)
	{
		clist = startlist(start, &l1);
		nlist = &l2;
	}
	else
	{
		clist = startlist(start, &l3);
		nlist = &l4;
	}

	for (; *s; s++){
		c = *s & 0xFF; //256
		step(clist, c, nlist);
		t = clist; clist = nlist; nlist = t;
	}
	return ismatch(clist);
}
///////////////////////////////////////////
//检查分隔符配置文件
int check_delimiter(char t)
{
	int flag = -1, i;

	for (i = 0; i < del_cnt; i++)
	{
		if (t == delimiter[i])
			flag = i;
	}
	return flag;
}

//检查配置文件的括号
int check_parenthesis(char t)
{
	int flag = -1, i;

	for (i = 0; i < par_cnt; i++)
	{
		if (t == par[i])
			flag = i;
	}
	return flag;
}


int check_quotes(char t)
{
	int flag = -1, i;

	if (t == '\'' || t == '"')
		flag = 1;

	return flag;
}


int keyword_search(char *token)
{
	int i, j, flag = -1, mat = 0, len = strlen(token);

	for (i = 0; i < key_cnt; i++)
	{
		mat = 0;
		for (j = 0; j < strlen(keywords[i]); j++)
		{
			if (j <= len && keywords[i][j] == token[j])
				mat++;//如果有一个字符相同就++
		}
		if (mat == strlen(keywords[i]))
		{
			flag = i;
			i = key_cnt;
		}
	}
	return flag;
}

//关系运算符
int relop_search(char *token)
{
	int i, j, flag = -1, mat = 0, len = strlen(token);

	for (i = 0; i < relop_cnt; i++)
	{
		mat = 0;
		for (j = 0; j < strlen(relop[i]); j++)
		{
			if (j < len && relop[i][j] == token[j])
				mat++;
		}
		if (mat == strlen(relop[i]))
		{
			flag = i;
			i = key_cnt;
		}
	}
	return flag;
}


int op_search(char *token)
{
	int i, j, flag = -1, mat = 0, len = strlen(token);

	for (i = 0; i < op_cnt; i++)
	{
		mat = 0;
		if (j < len && operators[i] == token[0])
			mat++;
		if (strlen(token) == 1 && mat == 1)
		{
			flag = i;
			i = key_cnt;
		}
	}
	return flag;
}



void save_list(char *temp, int type, int row, int col)
{
	if (table == NULL)
	{
		table = (sym_tab *)malloc(sizeof(sym_tab));
		table->next1 = NULL;
		strcpy(table->token, temp);
		table->type = type;

		loc *t12;
		t12 = (loc *)malloc(sizeof(loc));
		t12->row = row;
		t12->col = col;
		t12->next2 = NULL;

		table->list = t12;
	}
	else
	{
		sym_tab *t123, *last;
		t123 = table;
		int fl = 0;
		while (t123 != NULL)
		{
			if (t123->type == type)
			{
				if (strcmp(t123->token, temp) == 0)
					break;
			}
			last = t123;
			t123 = t123->next1;
		}
		if (t123 != NULL)
		{
			loc *t12;
			t12 = (loc *)malloc(sizeof(loc));
			t12->row = row;
			t12->col = col;
			t12->next2 = NULL;

			loc *l123;
			l123 = t123->list;

			while (l123->                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        next2 != NULL)
			{
				l123 = l123->next2;
			}
			l123->next2 = t12;
		}
		else
		{
			sym_tab *table1;
			table1 = (sym_tab *)malloc(sizeof(sym_tab));
			table1->next1 = NULL;
			strcpy(table1->token, temp);
			table->type = type;

			loc *t12;
			t12 = (loc *)malloc(sizeof(loc));
			t12->row = row;
			t12->col = col;
			t12->next2 = NULL;

			table->list = t12;

			last->next1 = table1;
		}
	}
}

int main()
{
	char regex[100], final[100], input[10][10], post_num[100], post_id[100];

}
