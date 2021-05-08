from distutils.core import setup

setup(
  name = 'veracode_api_py',         
  packages = ['veracode_api_py'],   
  version = '0.9.13',      
  license='MIT',        
  description = 'Python helper library for working with the Veracode APIs. Handles retries, pagination, and other features of the modern Veracode REST APIs.',   
  author = 'Tim Jarrett',                  
  author_email = 'tjarrett@veracode.com',      
  url = 'https://github.com/tjarrettveracode',   
  download_url = 'https://github.com/tjarrettveracode/veracode-api-py/archive/v_094.tar.gz',    
  keywords = ['veracode', 'veracode-api'],   
  install_requires=[            
          'veracode-api-signing'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3'
  ],
)