def compressor(api_url, output_name, filenames):
    ''' Here we use the minify API 
        js files need to be send to url = https://javascript-minifier.com/raw
        css files need to be send to url = https://cssminifier.com/raw
    '''
    code = []
    total_cost = 0
    for fn in filenames:
        if fn.startswith('http://') or fn.startswith('https://'):
            response = requests.get(fn)
            if response.status_code == 200:
                code.append( response.text )
            else:
                print 'ERROR: "%s" is not a valid url! Exit with status code %d' % (fn, response.status_code)
                return False
        else:
            if not os.path.isfile(fn):
                print 'ERROR: "%s" is not a valid file!' % fn
                return False
            code.append( open(fn).read().decode('utf-8') )
        cost = len(code[-1]) / 1024.0
        total_cost += cost
        print "added %s with (%.2fK)" % (fn, cost)

    payload = {'input': u' '.join(code)}
    response = requests.post(api_url, payload)
    if response.status_code == 200:
        outfile = open(output_name, 'w')
        outfile.write(response.text.encode('utf-8'))
        outfile.close()

        print '-' * 50
        print '>> output: %s (%.2fK) from (%.2fK)' % (output_name, len(response.text)/1024.0, total_cost)
        return 
    else:
        print 'ERROR: "%s" is not a valid url! Exit with status code %d' % (fn, response.status_code)
        return False
