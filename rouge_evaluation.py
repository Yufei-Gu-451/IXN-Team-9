from rouge import FilesRouge

files_rouge = FilesRouge()

average_score = {'rouge-1':{'r':0, 'p':0, 'f':0}, 'rouge-2':{'r':0, 'p':0, 'f':0}}

for i in range(1001, 2501):
    hyp_path = 'Abstracts/Abstract-' + str(i) + '.txt'
    ref_path = 'FullTexts/FullText-' + str(i) + '.txt'
    scores = files_rouge.get_scores(hyp_path=hyp_path, ref_path=ref_path, avg = True)
    print(i)

    average_score['rouge-1']['r'] += scores['rouge-1']['r']
    average_score['rouge-1']['p'] += scores['rouge-1']['p']
    average_score['rouge-1']['f'] += scores['rouge-1']['f']

    average_score['rouge-2']['r'] += scores['rouge-2']['r']
    average_score['rouge-2']['p'] += scores['rouge-2']['p']
    average_score['rouge-2']['f'] += scores['rouge-2']['f']

print('score[\'rouge-1\'][\'r\'] = ' + average_score['rouge-1']['r']/1500)
print('score[\'rouge-1\'][\'p\'] = ' +average_score['rouge-1']['p']/1500)
print('score[\'rouge-1\'][\'f\'] = ' +average_score['rouge-1']['f']/1500)
print('score[\'rouge-2\'][\'r\'] = ' +average_score['rouge-2']['r']/1500)
print('score[\'rouge-2\'][\'p\'] = ' +average_score['rouge-2']['p']/1500)
print('score[\'rouge-2\'][\'f\'] = ' +average_score['rouge-2']['f']/1500)


'''
score['rouge-1']['r'] = 0.06713925647564942
score['rouge-1']['p'] = 0.8004642481168254
score['rouge-1']['f'] = 0.12040021094700251
score['rouge-2']['r'] = 0.02408601014709728
score['rouge-2']['p'] = 0.44519501600899747
score['rouge-2']['f'] = 0.0445483952247947
'''