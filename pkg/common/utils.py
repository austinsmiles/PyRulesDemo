import logging
import inspect
log=logging

#log.basicConfig(level=log.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

log.basicConfig(level=log.INFO, format='%(asctime)s:%(filename)s:%(funcName)s'
                                      ':%(levelname)s :%(message)s')
