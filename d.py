import dask.bag as db
from dask.delayed import delayed
import ijson


bag = db.read_text('/tmp/oakland.geosjon')
print(bag.count().compute())
