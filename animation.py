# Author: Jinwei Lin
# Time: 06, Apirl, 2024 

import re
import argparse

# def get_index(astr, subStr):
#     try:
#         idx = astr.index(subStr)
#     except:
#         idx = -1
#     return idx


# def removeMidStr(astr, removeIdx):
#     return astr[:removeIdx[0]]+astr[removeIdx[1]+1:]


def replaceSubstr(astr, replaceIdx, replace='-'):
    return astr[:replaceIdx[0]] + replace*abs(replaceIdx[1]-replaceIdx[0]) + astr[replaceIdx[1]:] 


def getCommandContent(command):
    CommandContent = []

    pre_len_CommandContent = -1
    while(len(CommandContent) > pre_len_CommandContent):
        # print(f'{command = }')
        pre_len_CommandContent = len(CommandContent)

        # move 
        # e.g.: move 10 meters in X direction
        part = 'body'
        id = re.search(r'\s+move[sed]*\s+[\s0-9a-zA-Z]+in[\s\-a-zA-Z]+direction', command)
        if id:
            CommandContent.append(['move', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+moving\s+[\s0-9a-zA-Z]+in[\s\-a-zA-Z]+direction', command)
        if id:
            CommandContent.append(['move', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))


        # run or walk
        part = 'body'
        id = re.search(r'\s+r[au]n[s]*\s*', command)
        if id:
            CommandContent.append(['run', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+running', command)
        if id:
            CommandContent.append(['run', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+walk[sed]*\s*', command)
        if id:
            CommandContent.append(['walk', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+walking[\sa-zA-Z]*[,.]+', command)
        if id:
            CommandContent.append(['walk', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))


        # head
        part = 'head'
        id = re.search(r'\s+raise[sd]*\s+[\sa-zA-Z]*'+part, command)
        if id:
            CommandContent.append(['raise', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+raising\s+[\sa-zA-Z]*'+part, command)
        if id:
            CommandContent.append(['raise', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+bow[sed]*\s+[\sa-zA-Z]*'+part, command)
        if id:
            CommandContent.append(['bow', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+bowing\s+[\sa-zA-Z]*'+part, command)
        if id:
            CommandContent.append(['bow', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+shake[sn]*\s+[\sa-zA-Z]*'+part, command)
        if id:
            CommandContent.append(['shake', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+shaking\s+[\sa-zA-Z]*'+part, command)
        if id:
            CommandContent.append(['shake', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+shook\s+[\sa-zA-Z]*'+part, command)
        if id:
            CommandContent.append(['shake', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+look[sed]*\s+left\s*', command)
        if id:
            CommandContent.append(['look left', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+looking\s+left\s*', command)
        if id:
            CommandContent.append(['look left', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+look[sed]*\s+right\s*', command)
        if id:
            CommandContent.append(['look right', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+looking\s+right\s*', command)
        if id:
            CommandContent.append(['look right', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))


        # hand
        part = 'hand'
        id = re.search(r'\s+raise[sd]*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['raise', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+raising\s*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['raise', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+put[s]*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['put_down', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+putting\s*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['put_down', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+wave[sd]*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['wave', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+waving\s*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['wave', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))


        # leg
        part = 'leg'
        id = re.search(r'\s+lift[sed]*\s+[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['lift', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+lifting\s+[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['lift', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        # put the leg down
        id = re.search(r'\s+put[s]*\s+down[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['put_down', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+putting\s+down[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['put_down', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+shake[sn]*[\sa-zA-Z]*'+part+'[s]*', command)



        # forearm
        part = 'forearm'
        id = re.search(r'\s+raise[sd]*\s+[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['raise', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+raising\s+[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['raise', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+put[s]*\s+down[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['put_down', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+putting\s*\s+down[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['put_down', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+wave[sd]*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['wave', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+waving\s*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['wave', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))


        # calf
        part = 'calf'
        id = re.search(r'\s+lift[sd]*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['lift', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+raising\s*[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['lift', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+put[s]*\s+down[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['put_down', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))
        id = re.search(r'\s+putting\s*\s+down[\sa-zA-Z]*'+part+'[s]*', command)
        if id:
            CommandContent.append(['put_down', part, id.span()])
            command = replaceSubstr(command, (id.span()[0], id.span()[1]))


        # bend down/up
        for move1 in ['bend', 'bends', 'bending', 'bent']:
            for move2 in ['down', 'up']:
                id = re.search(move1 + r'\s+[\sa-zA-Z]*' + move2, command)
                if id:
                    CommandContent.append(['bend ' + move2, 'waist', id.span()])
                    command = replaceSubstr(command, (id.span()[0], id.span()[1]))

        # bend shrug shoulder
        for move1 in ['shrug', 'shrugs', 'shrugging', 'shrugged']:
            for move2 in ['shoulder', 'shoulders']:
                id = re.search(move1 + r'\s+[\sa-zA-Z]*' + move2, command)
                if id:
                    CommandContent.append(['shrug', 'shoulders', id.span()])
                    command = replaceSubstr(command, (id.span()[0], id.span()[1]))


        # turn left/right
        for move1 in ['turn', 'turns', 'turning', 'turned']:
            for move2 in ['left', 'right']:
                id = re.search(move1 + r'\s+[\sa-zA-Z]*' + move2, command)
                if id:
                    CommandContent.append(['turn ' + move2, 'body', id.span()])
                    command = replaceSubstr(command, (id.span()[0], id.span()[1]))

        # jump up/down
        for move1 in ['jump', 'jumps', 'jumping', 'jumped']:
            for move2 in ['up', 'dwon']:
                id = re.search(move1 + r'\s+[\sa-zA-Z]*' + move2, command)
                if id:
                    CommandContent.append(['jump ' + move2, 'body', id.span()])
                    command = replaceSubstr(command, (id.span()[0], id.span()[1]))

        # ===========================================================================
        # complex actions:
        # punch
        for move1 in ['punch', 'punches', 'punching', 'punched']:
            id = re.search(move1 + r'\s*', command)
            if id:
                CommandContent.append(['punch' , 'body', id.span()])
                command = replaceSubstr(command, (id.span()[0], id.span()[1]))

        # push
        for move1 in ['push', 'pushes', 'pushing', 'pushed']:
            id = re.search(move1 + r'\s*', command)
            if id:
                CommandContent.append(['push' , 'body', id.span()])
                command = replaceSubstr(command, (id.span()[0], id.span()[1]))

        # push
        for move1 in ['push', 'pushes', 'pushing', 'pushed']:
            id = re.search(move1 + r'\s*', command)
            if id:
                CommandContent.append(['push', 'body', id.span()])
                command = replaceSubstr(command, (id.span()[0], id.span()[1]))

        # left/right kick
        for move1 in ['left', 'right']:
            for move2 in ['kick']:
                id = re.search(move1 + r'\s+[\sa-zA-Z]*' + move2, command)
                if id:
                    CommandContent.append([move1, move2, id.span()])
                    command = replaceSubstr(command, (id.span()[0], id.span()[1]))

        # left/right hook
        for move1 in ['left', 'right']:
            for move2 in ['hook']:
                id = re.search(move1 + r'\s+[\sa-zA-Z]*' + move2, command)
                if id:
                    CommandContent.append([move1, move2, id.span()])
                    command = replaceSubstr(command, (id.span()[0], id.span()[1]))

        # kung fu
        for move1 in ['kick']:
            id = re.search(r'\s+kung fu\s+', command)
            if id:
                CommandContent.append(['kung fu', 'body', id.span()])
                command = replaceSubstr(command, (id.span()[0], id.span()[1]))

       

    # print()
    # print(f'{len(CommandContent) = }')
    # print(f'{pre_len_CommandContent = }')


    return CommandContent



def animation(command):
    print(f'{command = }')

    command_L = getCommandContent(command)
    print(f'{command_L = }')

    with open('./commands/command.txt', 'w+') as f:
        for item in command_L:
            f.write(str(item[0]) + '\n')
            f.write(str(item[1]) + '\n')
            for i in range(len(item[2])):
                f.write(str(item[2][i]) + '\n')

    with open('./commands/command_words.txt', 'w+') as f:
        f.write(str(command))
    return command_L






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate the commands list.')
    parser.add_argument("--command", required=True, default='', help="text of the command.")

    args = parser.parse_args()

    animation(args.command)


    # command = 'The object moves 2 miles in x direction. '
    # command = 'The object moves 2 miles in -x direction.'
    # command = 'The object ran 3 steps tiems seconds to the car'
    # command = 'Big: The object moves 2 miles in x direction, ran 4 steps tiems seconds to the car'
    # command = 'Big: The object walked 2 steps tiems and ran 3 steps tiems seconds to the car'
    
    # command = 'The object raises his head to the car'
    # command = 'The object bowed his head to the car'
    # command = 'The object bowed his head 20.12 degree to the car'
    # command = 'The object raises his head 20.12 degrees to the car'
    # command = 'Big: The object bowed his head 20 degrees and raises his head 66 degrees to the car'
    
    # command = 'The object shakes his head 60 degrees to the car'
    # command = 'The object raises his head 20.12 degrees and shakes his head 60 degrees to the car'
    # command = 'Big: The object raises his head 50 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, to the car'
    
    # command = 'The object looks left to the car'
    # command = 'The object looks left 22.33 degrees to the car'
    # command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, to the car'

    # command = 'The object looks right to the car'
    # command = 'The object looks right 22.33 degrees to the car'
    # command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, to the car'
    
    # command = 'The object raised his left hand to the car'
    # command = 'The object raised raised his right hand, raised his left hand 60 degrees to the car'
    # # command = 'The object raised his right hand 30 degrees to the car'
    # command = 'The object raised raised his left hand 60 degrees and raised his right hand 30 degrees to the car'
    # command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 60 degrees, raised his right hand 30 degrees, to the car'

    # command = 'The object puts down his left hand 60 degrees to the car'
    # command = 'The object puts down his right hand 80 degrees to the car'
    # command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 60 degrees, raised his right hand 30 degrees, put down his left hand 30 degrees, to the car'

    # command = 'The object waves his left hand 60 degrees to the car'
    # command = 'The object waves his right hand 60 degrees to the car'
    # command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 60 degrees, raised his right hand 30 degrees, put down his left hand 30 degrees, waves his left hand 60 degrees, waves his right hand 60 degrees, to the car'
    
    # command = 'The object lifts his left leg 60 degrees to the car'
    # command = 'The object lifts his right leg 60 degrees to the car'
    # command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 60 degrees, raised his right hand 30 degrees, put down his left hand 30 degrees, waves his left hand 60 degrees, waves his right hand 60 degrees, lift his left leg 60 degrees, lift his right leg 60 degrees, to the car'
    # command = 'The object puts down his left leg to the car, puts down his right leg 60 degrees to the car'
    # command = 'The object puts down his left leg to the car'
    # command = 'The object puts down his left leg 60 degrees to the car'
    # command = 'The object puts down his right leg 60 degrees to the car'
    # command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 60 degrees, raised his right hand 30 degrees, put down his left hand 30 degrees, waves his left hand 60 degrees, waves his right hand 60 degrees, lift his left leg 60 degrees, lift his right leg 60 degrees, puts down his left leg 60 degrees, puts down his right leg 60 degrees, puts down his left leg, to the car'

    # command = 'The object raises his left forearm to the car'
    # command = 'The object raises his left forearm 60 degrees to the car'
    # command = 'The object raises his right forearm to the car'
    # command = 'The object raises his right forearm 60 degrees to the car'
    # command = 'The object puts down his left forearm to the car'
    # command = 'The object puts down his left forearm 60 degrees to the car'
    # command = 'The object puts down his right forearm to the car'
    # command = 'The object puts down his right forearm 60 degrees to the car'
    # command = 'The object waves his left forearm to the car'
    # command = 'The object waves his right forearm to the car'
    # command = 'The object waves his left forearm 45 degrees to the car'
    # command = 'The object waves his right forearm 45 degrees to the car'
    # command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 20 degrees, raised his right hand 20 degrees, put down his left hand 30 degrees, put down his right hand 30 degrees, waves his left hand 60 degrees, waves his right hand 60 degrees, lift his left leg 60 degrees, lift his right leg 60 degrees, puts down his left leg 60 degrees, puts down his right leg 60 degrees, puts down his left leg, lifts his left leg, raises his left forearm 30 degrees, raises his right forearm 30 degrees, puts down his left forearm 30 degrees, puts down his right forearm 30 degrees, wave his left forearm 45 degrees, wave his right forearm 45 degrees, to the car'

    
    # command = 'The object puts down his left calf 60 degrees to the car'
    # command = 'The object puts down his right calf 60 degrees to the car'
    # command = 'The object lifts his left calf 60 degrees to the car'
    # command = 'The object lifts his right calf 60 degrees to the car'
    # command = 'The object puts down his left calf to the car'
    # command = 'The object puts down his right calf to the car'
    # command = 'The object lifts his left calf to the car'
    # command = 'The object lifts his right calf to the car'
    command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 20 degrees, raised his right hand 20 degrees, put down his left hand 30 degrees, put down his right hand 30 degrees, waves his left hand 60 degrees, waves his right hand 60 degrees, lift his left leg 60 degrees, lift his right leg 60 degrees, puts down his left leg 60 degrees, puts down his right leg 60 degrees, puts down his left leg, lifts his left leg, raises his left forearm 30 degrees, raises his right forearm 30 degrees, puts down his left forearm 30 degrees, puts down his right forearm 30 degrees, wave his left forearm 45 degrees, wave his right forearm 45 degrees, puts down his left calf 20 degrees, puts down his right calf 20 degrees, lifts his left calf 20 degrees, lifts his right calf 20 degrees, puts down his left calf, puts down his right calf, lifts his left calf, lifts his right calf, to the car'


    
    
    # animation(command)







