from livereload import Server
import os
import mimetypes


def make_app(root='.'):
    def app(environ, start_response):
        path = environ.get('PATH_INFO', '/')
        if path == '/':
            path = '/index.html'

        file_path = os.path.join(root, path.lstrip('/'))

        # Clean URL: try appending .html
        if not os.path.exists(file_path) and os.path.exists(file_path + '.html'):
            file_path = file_path + '.html'

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'Not Found']

        content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        file_size = os.path.getsize(file_path)
        range_header = environ.get('HTTP_RANGE')

        if range_header:
            # Parse "bytes=start-end"
            byte_range = range_header.strip().replace('bytes=', '')
            start_str, _, end_str = byte_range.partition('-')
            start = int(start_str) if start_str else 0
            end = int(end_str) if end_str else file_size - 1
            end = min(end, file_size - 1)
            length = end - start + 1
            headers = [
                ('Content-Type', content_type),
                ('Content-Range', f'bytes {start}-{end}/{file_size}'),
                ('Content-Length', str(length)),
                ('Accept-Ranges', 'bytes'),
            ]
            start_response('206 Partial Content', headers)
            with open(file_path, 'rb') as f:
                f.seek(start)
                return [f.read(length)]
        else:
            headers = [
                ('Content-Type', content_type),
                ('Content-Length', str(file_size)),
                ('Accept-Ranges', 'bytes'),
            ]
            start_response('200 OK', headers)
            return [open(file_path, 'rb').read()]

    return app


server = Server(make_app())
server.watch('*.html')
server.watch('*.css')
server.watch('*.js')

port = 5500
import socket
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', port)) != 0:
            break
        print(f"Port {port} in use, trying {port + 1}...")
        port += 1

server.serve(port=port, host='127.0.0.1')
