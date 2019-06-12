def suite():
    import unittest
    # import tests.whatever

    loader = unittest.TestLoader()
    loadmodule = loader.loadTestsFromModule
    suite = unittest.TestSuite()

    # suite.addTests(loadmodule(tests.whatever))
    return suite
