
## Logging:

Log exceptions:

```
try:
    open('/path/to/does/not/exist', 'rb')
except Exception, e:
    logger.error('Failed to open file', exc_info=True)
```