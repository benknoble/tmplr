def suite():
    import unittest
    import tests.temple

    loader = unittest.TestLoader()
    loadmodule = loader.loadTestsFromModule
    suite = unittest.TestSuite()

    suite.addTests(loadmodule(tests.temple))
    return suite
