from cowsay import cowsay, list_cows, make_bubble, cowthink, Bubble 
import cmd
import shlex

def analyze(line):

    def check_val(arg, arg_name, dic):
        if arg[0] != '-':
            dic[arg_name] = arg
        else:
            raise ValueError(f'{arg_name} got wrong value: {arg}')

    diction = dict()
    words = shlex.split(line)
    wit = iter(words)
    for word in wit:
        match word:
            case '-e' | '--eyes':
                eye_string = next(wit)
                check_val(eye_string, 'eyes', diction)
            case '-T' | '--tongue':
                tongue_string = next(wit)
                check_val(tongue_string, 'tongue', diction)
            case '-f' | '--file':
                cow = next(wit)
                if cow in list_cows():
                    diction['cow'] = cow
                else:
                    raise ValueError('No such cow file')
            case _:
                message = word
                diction['message'] = message 
    return diction

class mycmd(cmd.Cmd):
    prompt = '>>'

    def do_list_cows(self, arg):
        '''
        Lists all cow file names in the given directory
        ''' 
        print(list_cows())

    def do_cowthink(self, arg):
        '''
        cowthink(
            message: str,
            cow: str = 'default',
            preset: str = None,
            eyes: str = 'oo',
            tongue: str = '  ',
            width: int = 40,
            wrap_text: bool = True,
            cowfile: str = None
            ) -> str:

        Similar to the cowthink command. Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting
        cowthink string
        
        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param preset: -[bdgpstwy]
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        :param width: -W
        :param wrap_text: -n
        :param cowfile: a string containing the cow file text (chars are not
        decoded as they are in read_dot_cow) if this parameter is provided the
        cow parameter is ignored

        '''
        res = analyze(arg)
        print(cowthink(**res)) 

    def do_make_bubble(self, arg):
        ''' 
        make_bubble(
            self,
            text,
            brackets=Bubble(
                stem='\\',
                l='<',
                r='>',
                tl='/',
                tr='\\',
                ml='|',
                mr='|',
                bl='\\',
                br='/'
                ),
            width=40,
            wrap_text=True
            )
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        ''' 
        words = shlex.split(arg)
        params = dict()
        wit = iter(words)
        for word in wit:
            match word:
                case '--width':
                    width = next(wit)
                    check_val(width, 'width', params)
                case '--wrap_text':
                    wrap = next(wit)
                    check_val(wrap, 'wrap_text', params)
                case _:
                    message = word
                    diction['message'] = message  
        print(make_bubble(**params))

    def do_cowsay(
            self,
            message: str,
            cow: str = 'default',
            preset: str = None,
            eyes: str = 'oo',
            tongue: str = '  ',
            width: int = 40,
            wrap_text: bool = True,
            cowfile: str = None
            ) -> str:
        '''
        Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string

        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param preset: -[bdgpstwy]
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        :param width: -W
        :param wrap_text: -n
        :param cowfile: a string containing the cow file text (chars are not
        decoded as they are in read_dot_cow) if this parameter is provided the
        cow parameter is ignored
        '''
        res = analyze(message)
        print(cowsay(**res)) 

if __name__ == '__main__':
    mycmd().cmdloop()
