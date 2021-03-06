"use strict";
// Transcrypt'ed from Python, 2018-07-17 20:27:26
function app () {
    var __symbols__ = ['__py3.6__', '__esv5__'];
    var __all__ = {};
    var __world__ = __all__;
    var __nest__ = function (headObject, tailNames, value) {
        var current = headObject;
        if (tailNames != '') {
            var tailChain = tailNames.split ('.');
            var firstNewIndex = tailChain.length;
            for (var index = 0; index < tailChain.length; index++) {
                if (!current.hasOwnProperty (tailChain [index])) {
                    firstNewIndex = index;
                    break;
                }
                current = current [tailChain [index]];
            }
            for (var index = firstNewIndex; index < tailChain.length; index++) {
                current [tailChain [index]] = {};
                current = current [tailChain [index]];
            }
        }
        for (var attrib in value) {
            current [attrib] = value [attrib];
        }
    };
    __all__.__nest__ = __nest__;
    var __init__ = function (module) {
        if (!module.__inited__) {
            module.__all__.__init__ (module.__all__);
            module.__inited__ = true;
        }
        return module.__all__;
    };
    __all__.__init__ = __init__;
    var __get__ = function (self, func, quotedFuncName) {
        if (self) {
            if (self.hasOwnProperty ('__class__') || typeof self == 'string' || self instanceof String) {
                if (quotedFuncName) {
                    Object.defineProperty (self, quotedFuncName, {
                        value: function () {
                            var args = [] .slice.apply (arguments);
                            return func.apply (null, [self] .concat (args));
                        },
                        writable: true,
                        enumerable: true,
                        configurable: true
                    });
                }
                return function () {
                    var args = [] .slice.apply (arguments);
                    return func.apply (null, [self] .concat (args));
                };
            }
            else {
                return func;
            }
        }
        else {
            return func;
        }
    }
    __all__.__get__ = __get__;
    var __getcm__ = function (self, func, quotedFuncName) {
        if (self.hasOwnProperty ('__class__')) {
            return function () {
                var args = [] .slice.apply (arguments);
                return func.apply (null, [self.__class__] .concat (args));
            };
        }
        else {
            return function () {
                var args = [] .slice.apply (arguments);
                return func.apply (null, [self] .concat (args));
            };
        }
    }
    __all__.__getcm__ = __getcm__;
    var __getsm__ = function (self, func, quotedFuncName) {
        return func;
    }
    __all__.__getsm__ = __getsm__;
    var py_metatype = {
        __name__: 'type',
        __bases__: [],
        __new__: function (meta, name, bases, attribs) {
            var cls = function () {
                var args = [] .slice.apply (arguments);
                return cls.__new__ (args);
            };
            for (var index = bases.length - 1; index >= 0; index--) {
                var base = bases [index];
                for (var attrib in base) {
                    var descrip = Object.getOwnPropertyDescriptor (base, attrib);
                    Object.defineProperty (cls, attrib, descrip);
                }
            }
            cls.__metaclass__ = meta;
            cls.__name__ = name.startsWith ('py_') ? name.slice (3) : name;
            cls.__bases__ = bases;
            for (var attrib in attribs) {
                var descrip = Object.getOwnPropertyDescriptor (attribs, attrib);
                Object.defineProperty (cls, attrib, descrip);
            }
            return cls;
        }
    };
    py_metatype.__metaclass__ = py_metatype;
    __all__.py_metatype = py_metatype;
    var object = {
        __init__: function (self) {},
        __metaclass__: py_metatype,
        __name__: 'object',
        __bases__: [],
        __new__: function (args) {
            var instance = Object.create (this, {__class__: {value: this, enumerable: true}});
            this.__init__.apply (null, [instance] .concat (args));
            return instance;
        }
    };
    __all__.object = object;
    var __class__ = function (name, bases, attribs, meta) {
        if (meta === undefined) {
            meta = bases [0] .__metaclass__;
        }
        return meta.__new__ (meta, name, bases, attribs);
    }
    __all__.__class__ = __class__;
    var __pragma__ = function () {};
    __all__.__pragma__ = __pragma__;
	__nest__ (
		__all__,
		'org.transcrypt.__base__', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'org.transcrypt.__base__';
					var __Envir__ = __class__ ('__Envir__', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							self.interpreter_name = 'python';
							self.transpiler_name = 'transcrypt';
							self.transpiler_version = '3.6.101';
							self.target_subdir = '__javascript__';
						});}
					});
					var __envir__ = __Envir__ ();
					__pragma__ ('<all>')
						__all__.__Envir__ = __Envir__;
						__all__.__envir__ = __envir__;
						__all__.__name__ = __name__;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'org.transcrypt.__standard__', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'org.transcrypt.__standard__';
					var Exception = __class__ ('Exception', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							var kwargs = dict ();
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'self': var self = __allkwargs0__ [__attrib0__]; break;
											default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
										}
									}
									delete kwargs.__kwargtrans__;
								}
								var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
							}
							else {
								var args = tuple ();
							}
							self.__args__ = args;
							try {
								self.stack = kwargs.error.stack;
							}
							catch (__except0__) {
								self.stack = 'No stack trace available';
							}
						});},
						get __repr__ () {return __get__ (this, function (self) {
							if (len (self.__args__)) {
								return '{}{}'.format (self.__class__.__name__, repr (tuple (self.__args__)));
							}
							else {
								return '{}()'.format (self.__class__.__name__);
							}
						});},
						get __str__ () {return __get__ (this, function (self) {
							if (len (self.__args__) > 1) {
								return str (tuple (self.__args__));
							}
							else if (len (self.__args__)) {
								return str (self.__args__ [0]);
							}
							else {
								return '';
							}
						});}
					});
					var IterableError = __class__ ('IterableError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, error) {
							Exception.__init__ (self, "Can't iterate over non-iterable", __kwargtrans__ ({error: error}));
						});}
					});
					var StopIteration = __class__ ('StopIteration', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, error) {
							Exception.__init__ (self, 'Iterator exhausted', __kwargtrans__ ({error: error}));
						});}
					});
					var ValueError = __class__ ('ValueError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var KeyError = __class__ ('KeyError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var AssertionError = __class__ ('AssertionError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							if (message) {
								Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
							}
							else {
								Exception.__init__ (self, __kwargtrans__ ({error: error}));
							}
						});}
					});
					var NotImplementedError = __class__ ('NotImplementedError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var IndexError = __class__ ('IndexError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var AttributeError = __class__ ('AttributeError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var py_TypeError = __class__ ('py_TypeError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var Warning = __class__ ('Warning', [Exception], {
						__module__: __name__,
					});
					var UserWarning = __class__ ('UserWarning', [Warning], {
						__module__: __name__,
					});
					var DeprecationWarning = __class__ ('DeprecationWarning', [Warning], {
						__module__: __name__,
					});
					var RuntimeWarning = __class__ ('RuntimeWarning', [Warning], {
						__module__: __name__,
					});
					var __sort__ = function (iterable, key, reverse) {
						if (typeof key == 'undefined' || (key != null && key .hasOwnProperty ("__kwargtrans__"))) {;
							var key = null;
						};
						if (typeof reverse == 'undefined' || (reverse != null && reverse .hasOwnProperty ("__kwargtrans__"))) {;
							var reverse = false;
						};
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
									switch (__attrib0__) {
										case 'iterable': var iterable = __allkwargs0__ [__attrib0__]; break;
										case 'key': var key = __allkwargs0__ [__attrib0__]; break;
										case 'reverse': var reverse = __allkwargs0__ [__attrib0__]; break;
									}
								}
							}
						}
						else {
						}
						if (key) {
							iterable.sort ((function __lambda__ (a, b) {
								if (arguments.length) {
									var __ilastarg0__ = arguments.length - 1;
									if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
										var __allkwargs0__ = arguments [__ilastarg0__--];
										for (var __attrib0__ in __allkwargs0__) {
											switch (__attrib0__) {
												case 'a': var a = __allkwargs0__ [__attrib0__]; break;
												case 'b': var b = __allkwargs0__ [__attrib0__]; break;
											}
										}
									}
								}
								else {
								}
								return (key (a) > key (b) ? 1 : -(1));
							}));
						}
						else {
							iterable.sort ();
						}
						if (reverse) {
							iterable.reverse ();
						}
					};
					var sorted = function (iterable, key, reverse) {
						if (typeof key == 'undefined' || (key != null && key .hasOwnProperty ("__kwargtrans__"))) {;
							var key = null;
						};
						if (typeof reverse == 'undefined' || (reverse != null && reverse .hasOwnProperty ("__kwargtrans__"))) {;
							var reverse = false;
						};
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
									switch (__attrib0__) {
										case 'iterable': var iterable = __allkwargs0__ [__attrib0__]; break;
										case 'key': var key = __allkwargs0__ [__attrib0__]; break;
										case 'reverse': var reverse = __allkwargs0__ [__attrib0__]; break;
									}
								}
							}
						}
						else {
						}
						if (py_typeof (iterable) == dict) {
							var result = copy (iterable.py_keys ());
						}
						else {
							var result = copy (iterable);
						}
						__sort__ (result, key, reverse);
						return result;
					};
					var map = function (func, iterable) {
						return (function () {
							var __accu0__ = [];
							var __iterable0__ = iterable;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var item = __iterable0__ [__index0__];
								__accu0__.append (func (item));
							}
							return __accu0__;
						}) ();
					};
					var filter = function (func, iterable) {
						if (func == null) {
							var func = bool;
						}
						return (function () {
							var __accu0__ = [];
							var __iterable0__ = iterable;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var item = __iterable0__ [__index0__];
								if (func (item)) {
									__accu0__.append (item);
								}
							}
							return __accu0__;
						}) ();
					};
					var __Terminal__ = __class__ ('__Terminal__', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							self.buffer = '';
							try {
								self.element = document.getElementById ('__terminal__');
							}
							catch (__except0__) {
								self.element = null;
							}
							if (self.element) {
								self.element.style.overflowX = 'auto';
								self.element.style.boxSizing = 'border-box';
								self.element.style.padding = '5px';
								self.element.innerHTML = '_';
							}
						});},
						get print () {return __get__ (this, function (self) {
							var sep = ' ';
							var end = '\n';
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'self': var self = __allkwargs0__ [__attrib0__]; break;
											case 'sep': var sep = __allkwargs0__ [__attrib0__]; break;
											case 'end': var end = __allkwargs0__ [__attrib0__]; break;
										}
									}
								}
								var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
							}
							else {
								var args = tuple ();
							}
							self.buffer = '{}{}{}'.format (self.buffer, sep.join ((function () {
								var __accu0__ = [];
								var __iterable0__ = args;
								for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
									var arg = __iterable0__ [__index0__];
									__accu0__.append (str (arg));
								}
								return __accu0__;
							}) ()), end).__getslice__ (-(4096), null, 1);
							if (self.element) {
								self.element.innerHTML = self.buffer.py_replace ('\n', '<br>').py_replace (' ', '&nbsp');
								self.element.scrollTop = self.element.scrollHeight;
							}
							else {
								console.log (sep.join ((function () {
									var __accu0__ = [];
									var __iterable0__ = args;
									for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
										var arg = __iterable0__ [__index0__];
										__accu0__.append (str (arg));
									}
									return __accu0__;
								}) ()));
							}
						});},
						get input () {return __get__ (this, function (self, question) {
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'self': var self = __allkwargs0__ [__attrib0__]; break;
											case 'question': var question = __allkwargs0__ [__attrib0__]; break;
										}
									}
								}
							}
							else {
							}
							self.print ('{}'.format (question), __kwargtrans__ ({end: ''}));
							var answer = window.prompt ('\n'.join (self.buffer.py_split ('\n').__getslice__ (-(16), null, 1)));
							self.print (answer);
							return answer;
						});}
					});
					var __terminal__ = __Terminal__ ();
					__pragma__ ('<all>')
						__all__.AssertionError = AssertionError;
						__all__.AttributeError = AttributeError;
						__all__.DeprecationWarning = DeprecationWarning;
						__all__.Exception = Exception;
						__all__.IndexError = IndexError;
						__all__.IterableError = IterableError;
						__all__.KeyError = KeyError;
						__all__.NotImplementedError = NotImplementedError;
						__all__.RuntimeWarning = RuntimeWarning;
						__all__.StopIteration = StopIteration;
						__all__.py_TypeError = py_TypeError;
						__all__.UserWarning = UserWarning;
						__all__.ValueError = ValueError;
						__all__.Warning = Warning;
						__all__.__Terminal__ = __Terminal__;
						__all__.__name__ = __name__;
						__all__.__sort__ = __sort__;
						__all__.__terminal__ = __terminal__;
						__all__.filter = filter;
						__all__.map = map;
						__all__.sorted = sorted;
					__pragma__ ('</all>')
				}
			}
		}
	);

    var __call__ = function (/* <callee>, <this>, <params>* */) {
        var args = [] .slice.apply (arguments);
        if (typeof args [0] == 'object' && '__call__' in args [0]) {
            return args [0] .__call__ .apply (args [1], args.slice (2));
        }
        else {
            return args [0] .apply (args [1], args.slice (2));
        }
    };
    __all__.__call__ = __call__;
    __nest__ (__all__, '', __init__ (__all__.org.transcrypt.__base__));
    var __envir__ = __all__.__envir__;
    __nest__ (__all__, '', __init__ (__all__.org.transcrypt.__standard__));
    var Exception = __all__.Exception;
    var IterableError = __all__.IterableError;
    var StopIteration = __all__.StopIteration;
    var ValueError = __all__.ValueError;
    var KeyError = __all__.KeyError;
    var AssertionError = __all__.AssertionError;
    var NotImplementedError = __all__.NotImplementedError;
    var IndexError = __all__.IndexError;
    var AttributeError = __all__.AttributeError;
    var py_TypeError = __all__.py_TypeError;
    var Warning = __all__.Warning;
    var UserWarning = __all__.UserWarning;
    var DeprecationWarning = __all__.DeprecationWarning;
    var RuntimeWarning = __all__.RuntimeWarning;
    var __sort__ = __all__.__sort__;
    var sorted = __all__.sorted;
    var map = __all__.map;
    var filter = __all__.filter;
    __all__.print = __all__.__terminal__.print;
    __all__.input = __all__.__terminal__.input;
    var __terminal__ = __all__.__terminal__;
    var print = __all__.print;
    var input = __all__.input;
    __envir__.executor_name = __envir__.transpiler_name;
    var __main__ = {__file__: ''};
    __all__.main = __main__;
    var __except__ = null;
    __all__.__except__ = __except__;
    var __kwargtrans__ = function (anObject) {
        anObject.__kwargtrans__ = null;
        anObject.constructor = Object;
        return anObject;
    }
    __all__.__kwargtrans__ = __kwargtrans__;
    var __globals__ = function (anObject) {
        if (isinstance (anObject, dict)) {
            return anObject;
        }
        else {
            return dict (anObject)
        }
    }
    __all__.__globals__ = __globals__
    var __super__ = function (aClass, methodName) {
        for (var index = 0; index < aClass.__bases__.length; index++) {
            var base = aClass.__bases__ [index];
            if (methodName in base) {
               return base [methodName];
            }
        }
        throw new Exception ('Superclass method not found');
    }
    __all__.__super__ = __super__
    var property = function (getter, setter) {
        if (!setter) {
            setter = function () {};
        }
        return {get: function () {return getter (this)}, set: function (value) {setter (this, value)}, enumerable: true};
    }
    __all__.property = property;
    var __setProperty__ = function (anObject, name, descriptor) {
        if (!anObject.hasOwnProperty (name)) {
            Object.defineProperty (anObject, name, descriptor);
        }
    }
    __all__.__setProperty__ = __setProperty__
    function assert (condition, message) {
        if (!condition) {
            throw AssertionError (message, new Error ());
        }
    }
    __all__.assert = assert;
    var __merge__ = function (object0, object1) {
        var result = {};
        for (var attrib in object0) {
            result [attrib] = object0 [attrib];
        }
        for (var attrib in object1) {
            result [attrib] = object1 [attrib];
        }
        return result;
    };
    __all__.__merge__ = __merge__;
    var dir = function (obj) {
        var aList = [];
        for (var aKey in obj) {
            aList.push (aKey.startsWith ('py_') ? aKey.slice (3) : aKey);
        }
        aList.sort ();
        return aList;
    };
    __all__.dir = dir;
    var setattr = function (obj, name, value) {
        obj [name] = value;
    };
    __all__.setattr = setattr;
    var getattr = function (obj, name) {
        return name in obj ? obj [name] : obj ['py_' + name];
    };
    __all__.getattr = getattr;
    var hasattr = function (obj, name) {
        try {
            return name in obj || 'py_' + name in obj;
        }
        catch (exception) {
            return false;
        }
    };
    __all__.hasattr = hasattr;
    var delattr = function (obj, name) {
        if (name in obj) {
            delete obj [name];
        }
        else {
            delete obj ['py_' + name];
        }
    };
    __all__.delattr = (delattr);
    var __in__ = function (element, container) {
        if (container === undefined || container === null) {
            return false;
        }
        if (container.__contains__ instanceof Function) {
            return container.__contains__ (element);
        }
        else {
            return (
                container.indexOf ?
                container.indexOf (element) > -1 :
                container.hasOwnProperty (element)
            );
        }
    };
    __all__.__in__ = __in__;
    var __specialattrib__ = function (attrib) {
        return (attrib.startswith ('__') && attrib.endswith ('__')) || attrib == 'constructor' || attrib.startswith ('py_');
    };
    __all__.__specialattrib__ = __specialattrib__;
    var len = function (anObject) {
        if (anObject === undefined || anObject === null) {
            return 0;
        }
        if (anObject.__len__ instanceof Function) {
            return anObject.__len__ ();
        }
        if (anObject.length !== undefined) {
            return anObject.length;
        }
        var length = 0;
        for (var attr in anObject) {
            if (!__specialattrib__ (attr)) {
                length++;
            }
        }
        return length;
    };
    __all__.len = len;
    function __i__ (any) {
        return py_typeof (any) == dict ? any.py_keys () : any;
    }
    function __k__ (keyed, key) {
        var result = keyed [key];
        if (typeof result == 'undefined') {
            if (keyed instanceof Array)
                if (key == +key && key >= 0 && keyed.length > key)
                    return result;
                else
                    throw IndexError (key, new Error());
            else
                throw KeyError (key, new Error());
        }
        return result;
    }
    function __t__ (target) {
        return (
            target === undefined || target === null ? false :
            ['boolean', 'number'] .indexOf (typeof target) >= 0 ? target :
            target.__bool__ instanceof Function ? (target.__bool__ () ? target : false) :
            target.__len__ instanceof Function ?  (target.__len__ () !== 0 ? target : false) :
            target instanceof Function ? target :
            len (target) !== 0 ? target :
            false
        );
    }
    __all__.__t__ = __t__;
    var float = function (any) {
        if (any == 'inf') {
            return Infinity;
        }
        else if (any == '-inf') {
            return -Infinity;
        }
        else if (any == 'nan') {
            return NaN;
        }
        else if (isNaN (parseFloat (any))) {
            if (any === false) {
                return 0;
            }
            else if (any === true) {
                return 1;
            }
            else {
                throw ValueError ("could not convert string to float: '" + str(any) + "'", new Error ());
            }
        }
        else {
            return +any;
        }
    };
    float.__name__ = 'float';
    float.__bases__ = [object];
    __all__.float = float;
    var int = function (any) {
        return float (any) | 0
    };
    int.__name__ = 'int';
    int.__bases__ = [object];
    __all__.int = int;
    var bool = function (any) {
        return !!__t__ (any);
    };
    bool.__name__ = 'bool';
    bool.__bases__ = [int];
    __all__.bool = bool;
    var py_typeof = function (anObject) {
        var aType = typeof anObject;
        if (aType == 'object') {
            try {
                return '__class__' in anObject ? anObject.__class__ : object;
            }
            catch (exception) {
                return aType;
            }
        }
        else {
            return (
                aType == 'boolean' ? bool :
                aType == 'string' ? str :
                aType == 'number' ? (anObject % 1 == 0 ? int : float) :
                null
            );
        }
    };
    __all__.py_typeof = py_typeof;
    var issubclass = function (aClass, classinfo) {
        if (classinfo instanceof Array) {
            for (var index = 0; index < classinfo.length; index++) {
                var aClass2 = classinfo [index];
                if (issubclass (aClass, aClass2)) {
                    return true;
                }
            }
            return false;
        }
        try {
            var aClass2 = aClass;
            if (aClass2 == classinfo) {
                return true;
            }
            else {
                var bases = [].slice.call (aClass2.__bases__);
                while (bases.length) {
                    aClass2 = bases.shift ();
                    if (aClass2 == classinfo) {
                        return true;
                    }
                    if (aClass2.__bases__.length) {
                        bases = [].slice.call (aClass2.__bases__).concat (bases);
                    }
                }
                return false;
            }
        }
        catch (exception) {
            return aClass == classinfo || classinfo == object;
        }
    };
    __all__.issubclass = issubclass;
    var isinstance = function (anObject, classinfo) {
        try {
            return '__class__' in anObject ? issubclass (anObject.__class__, classinfo) : issubclass (py_typeof (anObject), classinfo);
        }
        catch (exception) {
            return issubclass (py_typeof (anObject), classinfo);
        }
    };
    __all__.isinstance = isinstance;
    var callable = function (anObject) {
        return anObject && typeof anObject == 'object' && '__call__' in anObject ? true : typeof anObject === 'function';
    };
    __all__.callable = callable;
    var repr = function (anObject) {
        try {
            return anObject.__repr__ ();
        }
        catch (exception) {
            try {
                return anObject.__str__ ();
            }
            catch (exception) {
                try {
                    if (anObject == null) {
                        return 'None';
                    }
                    else if (anObject.constructor == Object) {
                        var result = '{';
                        var comma = false;
                        for (var attrib in anObject) {
                            if (!__specialattrib__ (attrib)) {
                                if (attrib.isnumeric ()) {
                                    var attribRepr = attrib;
                                }
                                else {
                                    var attribRepr = '\'' + attrib + '\'';
                                }
                                if (comma) {
                                    result += ', ';
                                }
                                else {
                                    comma = true;
                                }
                                result += attribRepr + ': ' + repr (anObject [attrib]);
                            }
                        }
                        result += '}';
                        return result;
                    }
                    else {
                        return typeof anObject == 'boolean' ? anObject.toString () .capitalize () : anObject.toString ();
                    }
                }
                catch (exception) {
                    return '<object of type: ' + typeof anObject + '>';
                }
            }
        }
    };
    __all__.repr = repr;
    var chr = function (charCode) {
        return String.fromCharCode (charCode);
    };
    __all__.chr = chr;
    var ord = function (aChar) {
        return aChar.charCodeAt (0);
    };
    __all__.ord = ord;
    var max = function (nrOrSeq) {
        return arguments.length == 1 ? Math.max.apply (null, nrOrSeq) : Math.max.apply (null, arguments);
    };
    __all__.max = max;
    var min = function (nrOrSeq) {
        return arguments.length == 1 ? Math.min.apply (null, nrOrSeq) : Math.min.apply (null, arguments);
    };
    __all__.min = min;
    var abs = Math.abs;
    __all__.abs = abs;
    var round = function (number, ndigits) {
        if (ndigits) {
            var scale = Math.pow (10, ndigits);
            number *= scale;
        }
        var rounded = Math.round (number);
        if (rounded - number == 0.5 && rounded % 2) {
            rounded -= 1;
        }
        if (ndigits) {
            rounded /= scale;
        }
        return rounded;
    };
    __all__.round = round;
    function __jsUsePyNext__ () {
        try {
            var result = this.__next__ ();
            return {value: result, done: false};
        }
        catch (exception) {
            return {value: undefined, done: true};
        }
    }
    function __pyUseJsNext__ () {
        var result = this.next ();
        if (result.done) {
            throw StopIteration (new Error ());
        }
        else {
            return result.value;
        }
    }
    function py_iter (iterable) {
        if (typeof iterable == 'string' || '__iter__' in iterable) {
            var result = iterable.__iter__ ();
            result.next = __jsUsePyNext__;
        }
        else if ('selector' in iterable) {
            var result = list (iterable) .__iter__ ();
            result.next = __jsUsePyNext__;
        }
        else if ('next' in iterable) {
            var result = iterable
            if (! ('__next__' in result)) {
                result.__next__ = __pyUseJsNext__;
            }
        }
        else if (Symbol.iterator in iterable) {
            var result = iterable [Symbol.iterator] ();
            result.__next__ = __pyUseJsNext__;
        }
        else {
            throw IterableError (new Error ());
        }
        result [Symbol.iterator] = function () {return result;};
        return result;
    }
    function py_next (iterator) {
        try {
            var result = iterator.__next__ ();
        }
        catch (exception) {
            var result = iterator.next ();
            if (result.done) {
                throw StopIteration (new Error ());
            }
            else {
                return result.value;
            }
        }
        if (result == undefined) {
            throw StopIteration (new Error ());
        }
        else {
            return result;
        }
    }
    function __PyIterator__ (iterable) {
        this.iterable = iterable;
        this.index = 0;
    }
    __PyIterator__.prototype.__next__ = function () {
        if (this.index < this.iterable.length) {
            return this.iterable [this.index++];
        }
        else {
            throw StopIteration (new Error ());
        }
    };
    function __JsIterator__ (iterable) {
        this.iterable = iterable;
        this.index = 0;
    }
    __JsIterator__.prototype.next = function () {
        if (this.index < this.iterable.py_keys.length) {
            return {value: this.index++, done: false};
        }
        else {
            return {value: undefined, done: true};
        }
    };
    var py_reversed = function (iterable) {
        iterable = iterable.slice ();
        iterable.reverse ();
        return iterable;
    };
    __all__.py_reversed = py_reversed;
    var zip = function () {
        var args = [] .slice.call (arguments);
        for (var i = 0; i < args.length; i++) {
            if (typeof args [i] == 'string') {
                args [i] = args [i] .split ('');
            }
            else if (!Array.isArray (args [i])) {
                args [i] = Array.from (args [i]);
            }
        }
        var shortest = args.length == 0 ? [] : args.reduce (
            function (array0, array1) {
                return array0.length < array1.length ? array0 : array1;
            }
        );
        return shortest.map (
            function (current, index) {
                return args.map (
                    function (current) {
                        return current [index];
                    }
                );
            }
        );
    };
    __all__.zip = zip;
    function range (start, stop, step) {
        if (stop == undefined) {
            stop = start;
            start = 0;
        }
        if (step == undefined) {
            step = 1;
        }
        if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
            return [];
        }
        var result = [];
        for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
            result.push(i);
        }
        return result;
    };
    __all__.range = range;
    function any (iterable) {
        for (var index = 0; index < iterable.length; index++) {
            if (bool (iterable [index])) {
                return true;
            }
        }
        return false;
    }
    function all (iterable) {
        for (var index = 0; index < iterable.length; index++) {
            if (! bool (iterable [index])) {
                return false;
            }
        }
        return true;
    }
    function sum (iterable) {
        var result = 0;
        for (var index = 0; index < iterable.length; index++) {
            result += iterable [index];
        }
        return result;
    }
    __all__.any = any;
    __all__.all = all;
    __all__.sum = sum;
    function enumerate (iterable) {
        return zip (range (len (iterable)), iterable);
    }
    __all__.enumerate = enumerate;
    function copy (anObject) {
        if (anObject == null || typeof anObject == "object") {
            return anObject;
        }
        else {
            var result = {};
            for (var attrib in obj) {
                if (anObject.hasOwnProperty (attrib)) {
                    result [attrib] = anObject [attrib];
                }
            }
            return result;
        }
    }
    __all__.copy = copy;
    function deepcopy (anObject) {
        if (anObject == null || typeof anObject == "object") {
            return anObject;
        }
        else {
            var result = {};
            for (var attrib in obj) {
                if (anObject.hasOwnProperty (attrib)) {
                    result [attrib] = deepcopy (anObject [attrib]);
                }
            }
            return result;
        }
    }
    __all__.deepcopy = deepcopy;
    function list (iterable) {
        var instance = iterable ? [] .slice.apply (iterable) : [];
        return instance;
    }
    __all__.list = list;
    Array.prototype.__class__ = list;
    list.__name__ = 'list';
    list.__bases__ = [object];
    Array.prototype.__iter__ = function () {return new __PyIterator__ (this);};
    Array.prototype.__getslice__ = function (start, stop, step) {
        if (start < 0) {
            start = this.length + start;
        }
        if (stop == null) {
            stop = this.length;
        }
        else if (stop < 0) {
            stop = this.length + stop;
        }
        else if (stop > this.length) {
            stop = this.length;
        }
        var result = list ([]);
        for (var index = start; index < stop; index += step) {
            result.push (this [index]);
        }
        return result;
    };
    Array.prototype.__setslice__ = function (start, stop, step, source) {
        if (start < 0) {
            start = this.length + start;
        }
        if (stop == null) {
            stop = this.length;
        }
        else if (stop < 0) {
            stop = this.length + stop;
        }
        if (step == null) {
            Array.prototype.splice.apply (this, [start, stop - start] .concat (source));
        }
        else {
            var sourceIndex = 0;
            for (var targetIndex = start; targetIndex < stop; targetIndex += step) {
                this [targetIndex] = source [sourceIndex++];
            }
        }
    };
    Array.prototype.__repr__ = function () {
        if (this.__class__ == set && !this.length) {
            return 'set()';
        }
        var result = !this.__class__ || this.__class__ == list ? '[' : this.__class__ == tuple ? '(' : '{';
        for (var index = 0; index < this.length; index++) {
            if (index) {
                result += ', ';
            }
            result += repr (this [index]);
        }
        if (this.__class__ == tuple && this.length == 1) {
            result += ',';
        }
        result += !this.__class__ || this.__class__ == list ? ']' : this.__class__ == tuple ? ')' : '}';;
        return result;
    };
    Array.prototype.__str__ = Array.prototype.__repr__;
    Array.prototype.append = function (element) {
        this.push (element);
    };
    Array.prototype.py_clear = function () {
        this.length = 0;
    };
    Array.prototype.extend = function (aList) {
        this.push.apply (this, aList);
    };
    Array.prototype.insert = function (index, element) {
        this.splice (index, 0, element);
    };
    Array.prototype.remove = function (element) {
        var index = this.indexOf (element);
        if (index == -1) {
            throw ValueError ("list.remove(x): x not in list", new Error ());
        }
        this.splice (index, 1);
    };
    Array.prototype.index = function (element) {
        return this.indexOf (element);
    };
    Array.prototype.py_pop = function (index) {
        if (index == undefined) {
            return this.pop ();
        }
        else {
            return this.splice (index, 1) [0];
        }
    };
    Array.prototype.py_sort = function () {
        __sort__.apply  (null, [this].concat ([] .slice.apply (arguments)));
    };
    Array.prototype.__add__ = function (aList) {
        return list (this.concat (aList));
    };
    Array.prototype.__mul__ = function (scalar) {
        var result = this;
        for (var i = 1; i < scalar; i++) {
            result = result.concat (this);
        }
        return result;
    };
    Array.prototype.__rmul__ = Array.prototype.__mul__;
    function tuple (iterable) {
        var instance = iterable ? [] .slice.apply (iterable) : [];
        instance.__class__ = tuple;
        return instance;
    }
    __all__.tuple = tuple;
    tuple.__name__ = 'tuple';
    tuple.__bases__ = [object];
    function set (iterable) {
        var instance = [];
        if (iterable) {
            for (var index = 0; index < iterable.length; index++) {
                instance.add (iterable [index]);
            }
        }
        instance.__class__ = set;
        return instance;
    }
    __all__.set = set;
    set.__name__ = 'set';
    set.__bases__ = [object];
    Array.prototype.__bindexOf__ = function (element) {
        element += '';
        var mindex = 0;
        var maxdex = this.length - 1;
        while (mindex <= maxdex) {
            var index = (mindex + maxdex) / 2 | 0;
            var middle = this [index] + '';
            if (middle < element) {
                mindex = index + 1;
            }
            else if (middle > element) {
                maxdex = index - 1;
            }
            else {
                return index;
            }
        }
        return -1;
    };
    Array.prototype.add = function (element) {
        if (this.indexOf (element) == -1) {
            this.push (element);
        }
    };
    Array.prototype.discard = function (element) {
        var index = this.indexOf (element);
        if (index != -1) {
            this.splice (index, 1);
        }
    };
    Array.prototype.isdisjoint = function (other) {
        this.sort ();
        for (var i = 0; i < other.length; i++) {
            if (this.__bindexOf__ (other [i]) != -1) {
                return false;
            }
        }
        return true;
    };
    Array.prototype.issuperset = function (other) {
        this.sort ();
        for (var i = 0; i < other.length; i++) {
            if (this.__bindexOf__ (other [i]) == -1) {
                return false;
            }
        }
        return true;
    };
    Array.prototype.issubset = function (other) {
        return set (other.slice ()) .issuperset (this);
    };
    Array.prototype.union = function (other) {
        var result = set (this.slice () .sort ());
        for (var i = 0; i < other.length; i++) {
            if (result.__bindexOf__ (other [i]) == -1) {
                result.push (other [i]);
            }
        }
        return result;
    };
    Array.prototype.intersection = function (other) {
        this.sort ();
        var result = set ();
        for (var i = 0; i < other.length; i++) {
            if (this.__bindexOf__ (other [i]) != -1) {
                result.push (other [i]);
            }
        }
        return result;
    };
    Array.prototype.difference = function (other) {
        var sother = set (other.slice () .sort ());
        var result = set ();
        for (var i = 0; i < this.length; i++) {
            if (sother.__bindexOf__ (this [i]) == -1) {
                result.push (this [i]);
            }
        }
        return result;
    };
    Array.prototype.symmetric_difference = function (other) {
        return this.union (other) .difference (this.intersection (other));
    };
    Array.prototype.py_update = function () {
        var updated = [] .concat.apply (this.slice (), arguments) .sort ();
        this.py_clear ();
        for (var i = 0; i < updated.length; i++) {
            if (updated [i] != updated [i - 1]) {
                this.push (updated [i]);
            }
        }
    };
    Array.prototype.__eq__ = function (other) {
        if (this.length != other.length) {
            return false;
        }
        if (this.__class__ == set) {
            this.sort ();
            other.sort ();
        }
        for (var i = 0; i < this.length; i++) {
            if (this [i] != other [i]) {
                return false;
            }
        }
        return true;
    };
    Array.prototype.__ne__ = function (other) {
        return !this.__eq__ (other);
    };
    Array.prototype.__le__ = function (other) {
        return this.issubset (other);
    };
    Array.prototype.__ge__ = function (other) {
        return this.issuperset (other);
    };
    Array.prototype.__lt__ = function (other) {
        return this.issubset (other) && !this.issuperset (other);
    };
    Array.prototype.__gt__ = function (other) {
        return this.issuperset (other) && !this.issubset (other);
    };
    function bytearray (bytable, encoding) {
        if (bytable == undefined) {
            return new Uint8Array (0);
        }
        else {
            var aType = py_typeof (bytable);
            if (aType == int) {
                return new Uint8Array (bytable);
            }
            else if (aType == str) {
                var aBytes = new Uint8Array (len (bytable));
                for (var i = 0; i < len (bytable); i++) {
                    aBytes [i] = bytable.charCodeAt (i);
                }
                return aBytes;
            }
            else if (aType == list || aType == tuple) {
                return new Uint8Array (bytable);
            }
            else {
                throw py_TypeError;
            }
        }
    }
    var bytes = bytearray;
    __all__.bytearray = bytearray;
    __all__.bytes = bytearray;
    Uint8Array.prototype.__add__ = function (aBytes) {
        var result = new Uint8Array (this.length + aBytes.length);
        result.set (this);
        result.set (aBytes, this.length);
        return result;
    };
    Uint8Array.prototype.__mul__ = function (scalar) {
        var result = new Uint8Array (scalar * this.length);
        for (var i = 0; i < scalar; i++) {
            result.set (this, i * this.length);
        }
        return result;
    };
    Uint8Array.prototype.__rmul__ = Uint8Array.prototype.__mul__;
    function str (stringable) {
        if (typeof stringable === 'number')
            return stringable.toString();
        else {
            try {
                return stringable.__str__ ();
            }
            catch (exception) {
                try {
                    return repr (stringable);
                }
                catch (exception) {
                    return String (stringable);
                }
            }
        }
    };
    __all__.str = str;
    String.prototype.__class__ = str;
    str.__name__ = 'str';
    str.__bases__ = [object];
    String.prototype.__iter__ = function () {new __PyIterator__ (this);};
    String.prototype.__repr__ = function () {
        return (this.indexOf ('\'') == -1 ? '\'' + this + '\'' : '"' + this + '"') .py_replace ('\t', '\\t') .py_replace ('\n', '\\n');
    };
    String.prototype.__str__ = function () {
        return this;
    };
    String.prototype.capitalize = function () {
        return this.charAt (0).toUpperCase () + this.slice (1);
    };
    String.prototype.endswith = function (suffix) {
        if (suffix instanceof Array) {
            for (var i=0;i<suffix.length;i++) {
                if (this.slice (-suffix[i].length) == suffix[i])
                    return true;
            }
        } else
            return suffix == '' || this.slice (-suffix.length) == suffix;
        return false;
    };
    String.prototype.find  = function (sub, start) {
        return this.indexOf (sub, start);
    };
    String.prototype.__getslice__ = function (start, stop, step) {
        if (start < 0) {
            start = this.length + start;
        }
        if (stop == null) {
            stop = this.length;
        }
        else if (stop < 0) {
            stop = this.length + stop;
        }
        var result = '';
        if (step == 1) {
            result = this.substring (start, stop);
        }
        else {
            for (var index = start; index < stop; index += step) {
                result = result.concat (this.charAt(index));
            }
        }
        return result;
    };
    __setProperty__ (String.prototype, 'format', {
        get: function () {return __get__ (this, function (self) {
            var args = tuple ([] .slice.apply (arguments).slice (1));
            var autoIndex = 0;
            return self.replace (/\{(\w*)\}/g, function (match, key) {
                if (key == '') {
                    key = autoIndex++;
                }
                if (key == +key) {
                    return args [key] == undefined ? match : str (args [key]);
                }
                else {
                    for (var index = 0; index < args.length; index++) {
                        if (typeof args [index] == 'object' && args [index][key] != undefined) {
                            return str (args [index][key]);
                        }
                    }
                    return match;
                }
            });
        });},
        enumerable: true
    });
    String.prototype.isalnum = function () {
        return /^[0-9a-zA-Z]{1,}$/.test(this)
    }
    String.prototype.isalpha = function () {
        return /^[a-zA-Z]{1,}$/.test(this)
    }
    String.prototype.isdecimal = function () {
        return /^[0-9]{1,}$/.test(this)
    }
    String.prototype.isdigit = function () {
        return this.isdecimal()
    }
    String.prototype.islower = function () {
        return /^[a-z]{1,}$/.test(this)
    }
    String.prototype.isupper = function () {
        return /^[A-Z]{1,}$/.test(this)
    }
    String.prototype.isspace = function () {
        return /^[\s]{1,}$/.test(this)
    }
    String.prototype.isnumeric = function () {
        return !isNaN (parseFloat (this)) && isFinite (this);
    };
    String.prototype.join = function (strings) {
        return strings.join (this);
    };
    String.prototype.lower = function () {
        return this.toLowerCase ();
    };
    String.prototype.py_replace = function (old, aNew, maxreplace) {
        return this.split (old, maxreplace) .join (aNew);
    };
    String.prototype.lstrip = function () {
        return this.replace (/^\s*/g, '');
    };
    String.prototype.rfind = function (sub, start) {
        return this.lastIndexOf (sub, start);
    };
    String.prototype.rsplit = function (sep, maxsplit) {
        if (sep == undefined || sep == null) {
            sep = /\s+/;
            var stripped = this.strip ();
        }
        else {
            var stripped = this;
        }
        if (maxsplit == undefined || maxsplit == -1) {
            return stripped.split (sep);
        }
        else {
            var result = stripped.split (sep);
            if (maxsplit < result.length) {
                var maxrsplit = result.length - maxsplit;
                return [result.slice (0, maxrsplit) .join (sep)] .concat (result.slice (maxrsplit));
            }
            else {
                return result;
            }
        }
    };
    String.prototype.rstrip = function () {
        return this.replace (/\s*$/g, '');
    };
    String.prototype.py_split = function (sep, maxsplit) {
        if (sep == undefined || sep == null) {
            sep = /\s+/;
            var stripped = this.strip ();
        }
        else {
            var stripped = this;
        }
        if (maxsplit == undefined || maxsplit == -1) {
            return stripped.split (sep);
        }
        else {
            var result = stripped.split (sep);
            if (maxsplit < result.length) {
                return result.slice (0, maxsplit).concat ([result.slice (maxsplit).join (sep)]);
            }
            else {
                return result;
            }
        }
    };
    String.prototype.startswith = function (prefix) {
        if (prefix instanceof Array) {
            for (var i=0;i<prefix.length;i++) {
                if (this.indexOf (prefix [i]) == 0)
                    return true;
            }
        } else
            return this.indexOf (prefix) == 0;
        return false;
    };
    String.prototype.strip = function () {
        return this.trim ();
    };
    String.prototype.upper = function () {
        return this.toUpperCase ();
    };
    String.prototype.__mul__ = function (scalar) {
        var result = '';
        for (var i = 0; i < scalar; i++) {
            result = result + this;
        }
        return result;
    };
    String.prototype.__rmul__ = String.prototype.__mul__;
    function __contains__ (element) {
        return this.hasOwnProperty (element);
    }
    function __keys__ () {
        var keys = [];
        for (var attrib in this) {
            if (!__specialattrib__ (attrib)) {
                keys.push (attrib);
            }
        }
        return keys;
    }
    function __items__ () {
        var items = [];
        for (var attrib in this) {
            if (!__specialattrib__ (attrib)) {
                items.push ([attrib, this [attrib]]);
            }
        }
        return items;
    }
    function __del__ (key) {
        delete this [key];
    }
    function __clear__ () {
        for (var attrib in this) {
            delete this [attrib];
        }
    }
    function __getdefault__ (aKey, aDefault) {
        var result = this [aKey];
        if (result == undefined) {
            result = this ['py_' + aKey]
        }
        return result == undefined ? (aDefault == undefined ? null : aDefault) : result;
    }
    function __setdefault__ (aKey, aDefault) {
        var result = this [aKey];
        if (result != undefined) {
            return result;
        }
        var val = aDefault == undefined ? null : aDefault;
        this [aKey] = val;
        return val;
    }
    function __pop__ (aKey, aDefault) {
        var result = this [aKey];
        if (result != undefined) {
            delete this [aKey];
            return result;
        } else {
            if ( aDefault === undefined ) {
                throw KeyError (aKey, new Error());
            }
        }
        return aDefault;
    }
    function __popitem__ () {
        var aKey = Object.keys (this) [0];
        if (aKey == null) {
            throw KeyError ("popitem(): dictionary is empty", new Error ());
        }
        var result = tuple ([aKey, this [aKey]]);
        delete this [aKey];
        return result;
    }
    function __update__ (aDict) {
        for (var aKey in aDict) {
            this [aKey] = aDict [aKey];
        }
    }
    function __values__ () {
        var values = [];
        for (var attrib in this) {
            if (!__specialattrib__ (attrib)) {
                values.push (this [attrib]);
            }
        }
        return values;
    }
    function __dgetitem__ (aKey) {
        return this [aKey];
    }
    function __dsetitem__ (aKey, aValue) {
        this [aKey] = aValue;
    }
    function dict (objectOrPairs) {
        var instance = {};
        if (!objectOrPairs || objectOrPairs instanceof Array) {
            if (objectOrPairs) {
                for (var index = 0; index < objectOrPairs.length; index++) {
                    var pair = objectOrPairs [index];
                    if ( !(pair instanceof Array) || pair.length != 2) {
                        throw ValueError(
                            "dict update sequence element #" + index +
                            " has length " + pair.length +
                            "; 2 is required", new Error());
                    }
                    var key = pair [0];
                    var val = pair [1];
                    if (!(objectOrPairs instanceof Array) && objectOrPairs instanceof Object) {
                         if (!isinstance (objectOrPairs, dict)) {
                             val = dict (val);
                         }
                    }
                    instance [key] = val;
                }
            }
        }
        else {
            if (isinstance (objectOrPairs, dict)) {
                var aKeys = objectOrPairs.py_keys ();
                for (var index = 0; index < aKeys.length; index++ ) {
                    var key = aKeys [index];
                    instance [key] = objectOrPairs [key];
                }
            } else if (objectOrPairs instanceof Object) {
                instance = objectOrPairs;
            } else {
                throw ValueError ("Invalid type of object for dict creation", new Error ());
            }
        }
        __setProperty__ (instance, '__class__', {value: dict, enumerable: false, writable: true});
        __setProperty__ (instance, '__contains__', {value: __contains__, enumerable: false});
        __setProperty__ (instance, 'py_keys', {value: __keys__, enumerable: false});
        __setProperty__ (instance, '__iter__', {value: function () {new __PyIterator__ (this.py_keys ());}, enumerable: false});
        __setProperty__ (instance, Symbol.iterator, {value: function () {new __JsIterator__ (this.py_keys ());}, enumerable: false});
        __setProperty__ (instance, 'py_items', {value: __items__, enumerable: false});
        __setProperty__ (instance, 'py_del', {value: __del__, enumerable: false});
        __setProperty__ (instance, 'py_clear', {value: __clear__, enumerable: false});
        __setProperty__ (instance, 'py_get', {value: __getdefault__, enumerable: false});
        __setProperty__ (instance, 'py_setdefault', {value: __setdefault__, enumerable: false});
        __setProperty__ (instance, 'py_pop', {value: __pop__, enumerable: false});
        __setProperty__ (instance, 'py_popitem', {value: __popitem__, enumerable: false});
        __setProperty__ (instance, 'py_update', {value: __update__, enumerable: false});
        __setProperty__ (instance, 'py_values', {value: __values__, enumerable: false});
        __setProperty__ (instance, '__getitem__', {value: __dgetitem__, enumerable: false});
        __setProperty__ (instance, '__setitem__', {value: __dsetitem__, enumerable: false});
        return instance;
    }
    __all__.dict = dict;
    dict.__name__ = 'dict';
    dict.__bases__ = [object];
    function __setdoc__ (docString) {
        this.__doc__ = docString;
        return this;
    }
    __setProperty__ (Function.prototype, '__setdoc__', {value: __setdoc__, enumerable: false});
    var __jsmod__ = function (a, b) {
        if (typeof a == 'object' && '__mod__' in a) {
            return a.__mod__ (b);
        }
        else if (typeof b == 'object' && '__rmod__' in b) {
            return b.__rmod__ (a);
        }
        else {
            return a % b;
        }
    };
    __all__.__jsmod__ = __jsmod__;
    var __mod__ = function (a, b) {
        if (typeof a == 'object' && '__mod__' in a) {
            return a.__mod__ (b);
        }
        else if (typeof b == 'object' && '__rmod__' in b) {
            return b.__rmod__ (a);
        }
        else {
            return ((a % b) + b) % b;
        }
    };
    __all__.mod = __mod__;
    var __pow__ = function (a, b) {
        if (typeof a == 'object' && '__pow__' in a) {
            return a.__pow__ (b);
        }
        else if (typeof b == 'object' && '__rpow__' in b) {
            return b.__rpow__ (a);
        }
        else {
            return Math.pow (a, b);
        }
    };
    __all__.pow = __pow__;
    var __neg__ = function (a) {
        if (typeof a == 'object' && '__neg__' in a) {
            return a.__neg__ ();
        }
        else {
            return -a;
        }
    };
    __all__.__neg__ = __neg__;
    var __matmul__ = function (a, b) {
        return a.__matmul__ (b);
    };
    __all__.__matmul__ = __matmul__;
    var __mul__ = function (a, b) {
        if (typeof a == 'object' && '__mul__' in a) {
            return a.__mul__ (b);
        }
        else if (typeof b == 'object' && '__rmul__' in b) {
            return b.__rmul__ (a);
        }
        else if (typeof a == 'string') {
            return a.__mul__ (b);
        }
        else if (typeof b == 'string') {
            return b.__rmul__ (a);
        }
        else {
            return a * b;
        }
    };
    __all__.__mul__ = __mul__;
    var __truediv__ = function (a, b) {
        if (typeof a == 'object' && '__truediv__' in a) {
            return a.__truediv__ (b);
        }
        else if (typeof b == 'object' && '__rtruediv__' in b) {
            return b.__rtruediv__ (a);
        }
        else if (typeof a == 'object' && '__div__' in a) {
            return a.__div__ (b);
        }
        else if (typeof b == 'object' && '__rdiv__' in b) {
            return b.__rdiv__ (a);
        }
        else {
            return a / b;
        }
    };
    __all__.__truediv__ = __truediv__;
    var __floordiv__ = function (a, b) {
        if (typeof a == 'object' && '__floordiv__' in a) {
            return a.__floordiv__ (b);
        }
        else if (typeof b == 'object' && '__rfloordiv__' in b) {
            return b.__rfloordiv__ (a);
        }
        else if (typeof a == 'object' && '__div__' in a) {
            return a.__div__ (b);
        }
        else if (typeof b == 'object' && '__rdiv__' in b) {
            return b.__rdiv__ (a);
        }
        else {
            return Math.floor (a / b);
        }
    };
    __all__.__floordiv__ = __floordiv__;
    var __add__ = function (a, b) {
        if (typeof a == 'object' && '__add__' in a) {
            return a.__add__ (b);
        }
        else if (typeof b == 'object' && '__radd__' in b) {
            return b.__radd__ (a);
        }
        else {
            return a + b;
        }
    };
    __all__.__add__ = __add__;
    var __sub__ = function (a, b) {
        if (typeof a == 'object' && '__sub__' in a) {
            return a.__sub__ (b);
        }
        else if (typeof b == 'object' && '__rsub__' in b) {
            return b.__rsub__ (a);
        }
        else {
            return a - b;
        }
    };
    __all__.__sub__ = __sub__;
    var __lshift__ = function (a, b) {
        if (typeof a == 'object' && '__lshift__' in a) {
            return a.__lshift__ (b);
        }
        else if (typeof b == 'object' && '__rlshift__' in b) {
            return b.__rlshift__ (a);
        }
        else {
            return a << b;
        }
    };
    __all__.__lshift__ = __lshift__;
    var __rshift__ = function (a, b) {
        if (typeof a == 'object' && '__rshift__' in a) {
            return a.__rshift__ (b);
        }
        else if (typeof b == 'object' && '__rrshift__' in b) {
            return b.__rrshift__ (a);
        }
        else {
            return a >> b;
        }
    };
    __all__.__rshift__ = __rshift__;
    var __or__ = function (a, b) {
        if (typeof a == 'object' && '__or__' in a) {
            return a.__or__ (b);
        }
        else if (typeof b == 'object' && '__ror__' in b) {
            return b.__ror__ (a);
        }
        else {
            return a | b;
        }
    };
    __all__.__or__ = __or__;
    var __xor__ = function (a, b) {
        if (typeof a == 'object' && '__xor__' in a) {
            return a.__xor__ (b);
        }
        else if (typeof b == 'object' && '__rxor__' in b) {
            return b.__rxor__ (a);
        }
        else {
            return a ^ b;
        }
    };
    __all__.__xor__ = __xor__;
    var __and__ = function (a, b) {
        if (typeof a == 'object' && '__and__' in a) {
            return a.__and__ (b);
        }
        else if (typeof b == 'object' && '__rand__' in b) {
            return b.__rand__ (a);
        }
        else {
            return a & b;
        }
    };
    __all__.__and__ = __and__;
    var __eq__ = function (a, b) {
        if (typeof a == 'object' && '__eq__' in a) {
            return a.__eq__ (b);
        }
        else {
            return a == b;
        }
    };
    __all__.__eq__ = __eq__;
    var __ne__ = function (a, b) {
        if (typeof a == 'object' && '__ne__' in a) {
            return a.__ne__ (b);
        }
        else {
            return a != b
        }
    };
    __all__.__ne__ = __ne__;
    var __lt__ = function (a, b) {
        if (typeof a == 'object' && '__lt__' in a) {
            return a.__lt__ (b);
        }
        else {
            return a < b;
        }
    };
    __all__.__lt__ = __lt__;
    var __le__ = function (a, b) {
        if (typeof a == 'object' && '__le__' in a) {
            return a.__le__ (b);
        }
        else {
            return a <= b;
        }
    };
    __all__.__le__ = __le__;
    var __gt__ = function (a, b) {
        if (typeof a == 'object' && '__gt__' in a) {
            return a.__gt__ (b);
        }
        else {
            return a > b;
        }
    };
    __all__.__gt__ = __gt__;
    var __ge__ = function (a, b) {
        if (typeof a == 'object' && '__ge__' in a) {
            return a.__ge__ (b);
        }
        else {
            return a >= b;
        }
    };
    __all__.__ge__ = __ge__;
    var __imatmul__ = function (a, b) {
        if ('__imatmul__' in a) {
            return a.__imatmul__ (b);
        }
        else {
            return a.__matmul__ (b);
        }
    };
    __all__.__imatmul__ = __imatmul__;
    var __ipow__ = function (a, b) {
        if (typeof a == 'object' && '__pow__' in a) {
            return a.__ipow__ (b);
        }
        else if (typeof a == 'object' && '__ipow__' in a) {
            return a.__pow__ (b);
        }
        else if (typeof b == 'object' && '__rpow__' in b) {
            return b.__rpow__ (a);
        }
        else {
            return Math.pow (a, b);
        }
    };
    __all__.ipow = __ipow__;
    var __ijsmod__ = function (a, b) {
        if (typeof a == 'object' && '__imod__' in a) {
            return a.__ismod__ (b);
        }
        else if (typeof a == 'object' && '__mod__' in a) {
            return a.__mod__ (b);
        }
        else if (typeof b == 'object' && '__rpow__' in b) {
            return b.__rmod__ (a);
        }
        else {
            return a % b;
        }
    };
    __all__.ijsmod__ = __ijsmod__;
    var __imod__ = function (a, b) {
        if (typeof a == 'object' && '__imod__' in a) {
            return a.__imod__ (b);
        }
        else if (typeof a == 'object' && '__mod__' in a) {
            return a.__mod__ (b);
        }
        else if (typeof b == 'object' && '__rmod__' in b) {
            return b.__rmod__ (a);
        }
        else {
            return ((a % b) + b) % b;
        }
    };
    __all__.imod = __imod__;
    var __imul__ = function (a, b) {
        if (typeof a == 'object' && '__imul__' in a) {
            return a.__imul__ (b);
        }
        else if (typeof a == 'object' && '__mul__' in a) {
            return a = a.__mul__ (b);
        }
        else if (typeof b == 'object' && '__rmul__' in b) {
            return a = b.__rmul__ (a);
        }
        else if (typeof a == 'string') {
            return a = a.__mul__ (b);
        }
        else if (typeof b == 'string') {
            return a = b.__rmul__ (a);
        }
        else {
            return a *= b;
        }
    };
    __all__.__imul__ = __imul__;
    var __idiv__ = function (a, b) {
        if (typeof a == 'object' && '__idiv__' in a) {
            return a.__idiv__ (b);
        }
        else if (typeof a == 'object' && '__div__' in a) {
            return a = a.__div__ (b);
        }
        else if (typeof b == 'object' && '__rdiv__' in b) {
            return a = b.__rdiv__ (a);
        }
        else {
            return a /= b;
        }
    };
    __all__.__idiv__ = __idiv__;
    var __iadd__ = function (a, b) {
        if (typeof a == 'object' && '__iadd__' in a) {
            return a.__iadd__ (b);
        }
        else if (typeof a == 'object' && '__add__' in a) {
            return a = a.__add__ (b);
        }
        else if (typeof b == 'object' && '__radd__' in b) {
            return a = b.__radd__ (a);
        }
        else {
            return a += b;
        }
    };
    __all__.__iadd__ = __iadd__;
    var __isub__ = function (a, b) {
        if (typeof a == 'object' && '__isub__' in a) {
            return a.__isub__ (b);
        }
        else if (typeof a == 'object' && '__sub__' in a) {
            return a = a.__sub__ (b);
        }
        else if (typeof b == 'object' && '__rsub__' in b) {
            return a = b.__rsub__ (a);
        }
        else {
            return a -= b;
        }
    };
    __all__.__isub__ = __isub__;
    var __ilshift__ = function (a, b) {
        if (typeof a == 'object' && '__ilshift__' in a) {
            return a.__ilshift__ (b);
        }
        else if (typeof a == 'object' && '__lshift__' in a) {
            return a = a.__lshift__ (b);
        }
        else if (typeof b == 'object' && '__rlshift__' in b) {
            return a = b.__rlshift__ (a);
        }
        else {
            return a <<= b;
        }
    };
    __all__.__ilshift__ = __ilshift__;
    var __irshift__ = function (a, b) {
        if (typeof a == 'object' && '__irshift__' in a) {
            return a.__irshift__ (b);
        }
        else if (typeof a == 'object' && '__rshift__' in a) {
            return a = a.__rshift__ (b);
        }
        else if (typeof b == 'object' && '__rrshift__' in b) {
            return a = b.__rrshift__ (a);
        }
        else {
            return a >>= b;
        }
    };
    __all__.__irshift__ = __irshift__;
    var __ior__ = function (a, b) {
        if (typeof a == 'object' && '__ior__' in a) {
            return a.__ior__ (b);
        }
        else if (typeof a == 'object' && '__or__' in a) {
            return a = a.__or__ (b);
        }
        else if (typeof b == 'object' && '__ror__' in b) {
            return a = b.__ror__ (a);
        }
        else {
            return a |= b;
        }
    };
    __all__.__ior__ = __ior__;
    var __ixor__ = function (a, b) {
        if (typeof a == 'object' && '__ixor__' in a) {
            return a.__ixor__ (b);
        }
        else if (typeof a == 'object' && '__xor__' in a) {
            return a = a.__xor__ (b);
        }
        else if (typeof b == 'object' && '__rxor__' in b) {
            return a = b.__rxor__ (a);
        }
        else {
            return a ^= b;
        }
    };
    __all__.__ixor__ = __ixor__;
    var __iand__ = function (a, b) {
        if (typeof a == 'object' && '__iand__' in a) {
            return a.__iand__ (b);
        }
        else if (typeof a == 'object' && '__and__' in a) {
            return a = a.__and__ (b);
        }
        else if (typeof b == 'object' && '__rand__' in b) {
            return a = b.__rand__ (a);
        }
        else {
            return a &= b;
        }
    };
    __all__.__iand__ = __iand__;
    var __getitem__ = function (container, key) {
        if (typeof container == 'object' && '__getitem__' in container) {
            return container.__getitem__ (key);
        }
        else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
            return container [container.length + key];
        }
        else {
            return container [key];
        }
    };
    __all__.__getitem__ = __getitem__;
    var __setitem__ = function (container, key, value) {
        if (typeof container == 'object' && '__setitem__' in container) {
            container.__setitem__ (key, value);
        }
        else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
            container [container.length + key] = value;
        }
        else {
            container [key] = value;
        }
    };
    __all__.__setitem__ = __setitem__;
    var __getslice__ = function (container, lower, upper, step) {
        if (typeof container == 'object' && '__getitem__' in container) {
            return container.__getitem__ ([lower, upper, step]);
        }
        else {
            return container.__getslice__ (lower, upper, step);
        }
    };
    __all__.__getslice__ = __getslice__;
    var __setslice__ = function (container, lower, upper, step, value) {
        if (typeof container == 'object' && '__setitem__' in container) {
            container.__setitem__ ([lower, upper, step], value);
        }
        else {
            container.__setslice__ (lower, upper, step, value);
        }
    };
    __all__.__setslice__ = __setslice__;
	(function () {
		var __name__ = '__main__';
		var MAX_CONTENT_LENGTH = 1000;
		var MAX_LINE_LENGTH = 500;
		var MATE_SCORE = 10000;
		var MATE_LIMIT = MATE_SCORE * 0.9;
		var WINNING_MOVE_LIMIT = 1000;
		var DOUBLE_EXCLAM_LIMIT = 500;
		var EXCLAM_LIMIT = 350;
		var PROMISING_LIMIT = 250;
		var INTERESTING_LIMIT = 150;
		var DRAWISH_LIMIT = 80;
		var LICH_API_GAMES_EXPORT = 'games/export';
		var uci_variant_to_variantkey = function (uci_variant, chess960) {
			if (typeof chess960 == 'undefined' || (chess960 != null && chess960 .hasOwnProperty ("__kwargtrans__"))) {;
				var chess960 = false;
			};
			if (uci_variant == 'chess') {
				if (chess960) {
					return 'chess960';
				}
				else {
					return 'standard';
				}
			}
			if (uci_variant == 'giveaway') {
				return 'antichess';
			}
			if (uci_variant == 'kingofthehill') {
				return 'kingOfTheHill';
			}
			if (uci_variant == 'racingkings') {
				return 'racingKings';
			}
			if (uci_variant == '3check') {
				return 'threeCheck';
			}
			return uci_variant;
		};
		var scoreverbal = function (score) {
			if (abs (score) < MATE_LIMIT) {
				return str (score);
			}
			if (score >= 0) {
				return '#{}'.format (MATE_SCORE - score);
			}
			return '#{}'.format (-(MATE_SCORE) - score);
		};
		var scorecolor = function (score) {
			if (score > MATE_LIMIT) {
				return '#0f0';
			}
			if (score > WINNING_MOVE_LIMIT) {
				return '#0e0';
			}
			if (score > DOUBLE_EXCLAM_LIMIT) {
				return '#0c0';
			}
			if (score > EXCLAM_LIMIT) {
				return '#0a0';
			}
			if (score > PROMISING_LIMIT) {
				return '#090';
			}
			if (score > INTERESTING_LIMIT) {
				return '#070';
			}
			if (score > DRAWISH_LIMIT) {
				return '#050';
			}
			if (score > 0) {
				return '#033';
			}
			if (score > -(DRAWISH_LIMIT)) {
				return '#330';
			}
			if (score > -(INTERESTING_LIMIT)) {
				return '#500';
			}
			if (score > -(PROMISING_LIMIT)) {
				return '#900';
			}
			if (score > -(EXCLAM_LIMIT)) {
				return '#a00';
			}
			if (score > -(DOUBLE_EXCLAM_LIMIT)) {
				return '#c00';
			}
			if (score > WINNING_MOVE_LIMIT) {
				return '#e00';
			}
			return '#f00';
		};
		var View = __class__ ('View', [object], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, callback, value) {
				if (typeof value == 'undefined' || (value != null && value .hasOwnProperty ("__kwargtrans__"))) {;
					var value = null;
				};
				self.callback = callback;
				self.value = value;
			});},
			get py_get () {return __get__ (this, function (self) {
				return self.value;
			});},
			get set () {return __get__ (this, function (self, value) {
				self.value = value;
				self.callback ();
			});}
		});
		var xor = function (b1, b2) {
			if (b1 && b2) {
				return false;
			}
			if (b1 || b2) {
				return true;
			}
			return false;
		};
		var cpick = function (cond, vtrue, vfalse) {
			if (cond) {
				return vtrue;
			}
			return vfalse;
		};
		var simulateserverlag = function (range, min_lag) {
			if (typeof range == 'undefined' || (range != null && range .hasOwnProperty ("__kwargtrans__"))) {;
				var range = 1000;
			};
			if (typeof min_lag == 'undefined' || (min_lag != null && min_lag .hasOwnProperty ("__kwargtrans__"))) {;
				var min_lag = 10;
			};
			if (__in__ ('localhost', window.location.host)) {
				return int (min_lag + Math.random () * range);
			}
			return min_lag;
		};
		var choose = function (cond, choicetrue, choicefalse) {
			if (cond) {
				return choicetrue;
			}
			return choicefalse;
		};
		var Vect = __class__ ('Vect', [object], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, x, y) {
				try {
					self.x = float (x);
					self.y = float (y);
				}
				catch (__except0__) {
					self.x = 0.0;
					self.y = 0.0;
					print ('vect init failed on', x, y);
				}
			});},
			get p () {return __get__ (this, function (self, v) {
				return Vect (self.x + v.x, self.y + v.y);
			});},
			get s () {return __get__ (this, function (self, s) {
				return Vect (self.x * s, self.y * s);
			});},
			get m () {return __get__ (this, function (self, v) {
				return self.p (v.s (-(1)));
			});},
			get copy () {return __get__ (this, function (self) {
				return Vect (self.x, self.y);
			});},
			get __repr__ () {return __get__ (this, function (self) {
				return 'Vect[x: {}, y: {}]'.format (self.x, self.y);
			});}
		});
		var getClientVect = function (ev) {
			return Vect (ev.clientX, ev.clientY);
		};
		var getglobalcssvar = function (key) {
			return getComputedStyle (window.document.documentElement).getPropertyValue (key);
		};
		var getglobalcssvarpxint = function (key, py_default) {
			try {
				var px = getglobalcssvar (key);
				var pxint = int (px.py_replace ('px', ''));
				return pxint;
			}
			catch (__except0__) {
				return py_default;
			}
		};
		var striplonglines = function (content, maxlen) {
			if (typeof maxlen == 'undefined' || (maxlen != null && maxlen .hasOwnProperty ("__kwargtrans__"))) {;
				var maxlen = MAX_LINE_LENGTH;
			};
			var lines = content.py_split ('\n');
			var strippedlines = list ([]);
			var __iterable0__ = lines;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var line = __iterable0__ [__index0__];
				if (len (line) > maxlen) {
					var sline = '{} ... [ truncated {} characters ]'.format (line.substring (0, maxlen), len (line) - maxlen);
					strippedlines.append (sline);
				}
				else {
					strippedlines.append (line);
				}
			}
			var content = '\n'.join (strippedlines);
			return content;
		};
		var getScrollBarWidth = function () {
			var outer = document.createElement ('div');
			outer.style.visibility = 'hidden';
			outer.style.width = '100px';
			outer.style.msOverflowStyle = 'scrollbar';
			document.body.appendChild (outer);
			var widthNoScroll = outer.offsetWidth;
			outer.style.overflow = 'scroll';
			var inner = document.createElement ('div');
			inner.style.width = '100%';
			outer.appendChild (inner);
			var widthWithScroll = inner.offsetWidth;
			outer.parentNode.removeChild (outer);
			return widthNoScroll - widthWithScroll;
		};
		var randint = function (range) {
			return int (Math.random () * range);
		};
		var randscalarvalue = function (baselen, pluslen) {
			var len = baselen + randint (pluslen);
			var buff = '';
			for (var i = 0; i < len; i++) {
				if (__mod__ (i, 2) == 1) {
					buff += list (['a', 'e', 'i', 'o', 'u']) [randint (5)];
				}
				else {
					buff += list (['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']) [randint (21)];
				}
			}
			return buff;
		};
		var uid = function () {
			var uid = randscalarvalue (8, 0);
			return uid;
		};
		var getfromobj = function (obj, key, py_default) {
			if (__in__ (key, obj)) {
				return obj [key];
			}
			return py_default;
		};
		var patchclasses = function (selfref, args) {
			var py_items = args.py_get ('patchclasses', list ([]));
			var __iterable0__ = py_items;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var item = __iterable0__ [__index0__];
				var parts = item.py_split ('/');
				var membername = parts [0];
				var action = parts [1];
				var classname = parts [2];
				if (action == 'a') {
					selfref [membername].ac (classname);
				}
				else if (action == 'r') {
					selfref [membername].rc (classname);
				}
			}
		};
		var parsejson = function (jsonstr, callback, errcallback) {
			try {
				var obj = JSON.parse (jsonstr);
				callback (obj);
			}
			catch (__except0__) {
				errcallback ('error parsing json');
			}
		};
		var putjsonbin = function (json, id, callback, errcallback) {
			var method = 'POST';
			var url = 'https://api.jsonbin.io/b';
			if (id == 'local') {
				// pass;
			}
			else if (!(id === null)) {
				var url = (url + '/') + id;
				var method = 'PUT';
			}
			var args = {'method': method, 'headers': {'Content-Type': 'application/json', 'private': false}, 'body': json};
			fetch (url, args).then ((function __lambda__ (response) {
				return response.text ().then ((function __lambda__ (content) {
					return callback (content);
				}), (function __lambda__ (err) {
					return errcallback (err);
				}));
			}), (function __lambda__ (err) {
				return errcallback (err);
			}));
		};
		var getjsonbin = function (id, callback, errcallback, version) {
			if (typeof version == 'undefined' || (version != null && version .hasOwnProperty ("__kwargtrans__"))) {;
				var version = 'latest';
			};
			var args = {'method': 'GET', 'headers': {'Content-Type': 'application/json', 'private': false}};
			fetch ((('https://api.jsonbin.io/b/' + id) + '/') + version, args).then ((function __lambda__ (response) {
				return response.text ().then ((function __lambda__ (content) {
					return callback (content);
				}), (function __lambda__ (err) {
					return errcalback (err);
				}));
			}), (function __lambda__ (err) {
				return errcallback (err);
			}));
		};
		var getjson = function (path, callback, errcallback) {
			var args = {'method': 'GET', 'headers': {'Content-Type': 'application/json'}};
			fetch (path, args).then ((function __lambda__ (response) {
				return response.text ().then ((function __lambda__ (content) {
					return parsejson (content, callback, errcallback);
				}), (function __lambda__ (err) {
					return errcalback (err);
				}));
			}), (function __lambda__ (err) {
				return errcallback (err);
			}));
		};
		var lichapiget = function (path, token, callback, errcallback) {
			var args = {'method': 'GET'};
			if (!(token === null) && false) {
				args ['headers'] = {'Authorization': 'Bearer {}'.format (token)};
			}
			fetch ('https://lichess.org/' + path, args).then ((function __lambda__ (response) {
				return response.text ().then ((function __lambda__ (content) {
					return callback (content);
				}), (function __lambda__ (err) {
					return errcalback (err);
				}));
			}), (function __lambda__ (err) {
				return errcallback (err);
			}));
		};
		var SCROLL_BAR_WIDTH = getScrollBarWidth ();
		var ce = function (tag) {
			return document.createElement (tag);
		};
		var ge = function (id) {
			return document.getElementById (id);
		};
		var addEventListener = function (object, kind, callback) {
			object.addEventListener (kind, callback, false);
		};
		var e = __class__ ('e', [object], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, tag) {
				self.e = ce (tag);
			});},
			get bc () {return __get__ (this, function (self, color) {
				self.e.style.backgroundColor = color;
				return self;
			});},
			get cp () {return __get__ (this, function (self) {
				self.e.style.cursor = 'pointer';
				return self;
			});},
			get cbc () {return __get__ (this, function (self, cond, colortrue, colorfalse) {
				self.e.style.backgroundColor = cpick (cond, colortrue, colorfalse);
				return self;
			});},
			get c () {return __get__ (this, function (self, color) {
				self.e.style.color = color;
				return self;
			});},
			get cc () {return __get__ (this, function (self, cond, colortrue, colorfalse) {
				self.e.style.color = cpick (cond, colortrue, colorfalse);
				return self;
			});},
			get zi () {return __get__ (this, function (self, zindex) {
				self.e.style.zIndex = zindex;
				return self;
			});},
			get op () {return __get__ (this, function (self, opacity) {
				self.e.style.opacity = opacity;
				return self;
			});},
			get ms () {return __get__ (this, function (self) {
				self.e.style.fontFamily = 'monospace';
				return self;
			});},
			get a () {return __get__ (this, function (self, e) {
				self.e.appendChild (e.e);
				return self;
			});},
			get aa () {return __get__ (this, function (self, es) {
				var __iterable0__ = es;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var e = __iterable0__ [__index0__];
					self.a (e);
				}
				return self;
			});},
			get sa () {return __get__ (this, function (self, key, value) {
				self.e.setAttribute (key, value);
				return self;
			});},
			get ra () {return __get__ (this, function (self, key) {
				self.e.removeAttribute (key);
				return self;
			});},
			get srac () {return __get__ (this, function (self, cond, key, value) {
				if (cond) {
					self.sa (key, value);
				}
				else {
					self.ra (key);
				}
			});},
			get ga () {return __get__ (this, function (self, key) {
				return self.e.getAttribute (key);
			});},
			get sv () {return __get__ (this, function (self, value) {
				self.e.value = value;
				return self;
			});},
			get html () {return __get__ (this, function (self, value) {
				self.e.innerHTML = value;
				return self;
			});},
			get x () {return __get__ (this, function (self) {
				while (self.e.firstChild) {
					self.e.removeChild (self.e.firstChild);
				}
				return self;
			});},
			get w () {return __get__ (this, function (self, w) {
				self.e.style.width = w + 'px';
				return self;
			});},
			get mw () {return __get__ (this, function (self, w) {
				self.e.style.minWidth = w + 'px';
				return self;
			});},
			get h () {return __get__ (this, function (self, h) {
				self.e.style.height = h + 'px';
				return self;
			});},
			get mh () {return __get__ (this, function (self, h) {
				self.e.style.minHeight = h + 'px';
				return self;
			});},
			get t () {return __get__ (this, function (self, t) {
				self.e.style.top = t + 'px';
				return self;
			});},
			get l () {return __get__ (this, function (self, l) {
				self.e.style.left = l + 'px';
				return self;
			});},
			get cl () {return __get__ (this, function (self, cond, ltrue, lfalse) {
				self.e.style.left = cpick (cond, ltrue, lfalse) + 'px';
				return self;
			});},
			get ct () {return __get__ (this, function (self, cond, ttrue, tfalse) {
				self.e.style.top = cpick (cond, ttrue, tfalse) + 'px';
				return self;
			});},
			get pv () {return __get__ (this, function (self, v) {
				return self.l (v.x).t (v.y);
			});},
			get pa () {return __get__ (this, function (self) {
				self.e.style.position = 'absolute';
				return self;
			});},
			get pr () {return __get__ (this, function (self) {
				self.e.style.position = 'relative';
				return self;
			});},
			get ml () {return __get__ (this, function (self, ml) {
				self.e.style.marginLeft = ml + 'px';
				return self;
			});},
			get mr () {return __get__ (this, function (self, mr) {
				self.e.style.marginRight = mr + 'px';
				return self;
			});},
			get mt () {return __get__ (this, function (self, mt) {
				self.e.style.marginTop = mt + 'px';
				return self;
			});},
			get mb () {return __get__ (this, function (self, mb) {
				self.e.style.marginBottom = mb + 'px';
				return self;
			});},
			get ac () {return __get__ (this, function (self, klass) {
				self.e.classList.add (klass);
				return self;
			});},
			get acc () {return __get__ (this, function (self, cond, klass) {
				if (cond) {
					self.e.classList.add (klass);
				}
				return self;
			});},
			get aac () {return __get__ (this, function (self, klasses) {
				var __iterable0__ = klasses;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var klass = __iterable0__ [__index0__];
					self.e.classList.add (klass);
				}
				return self;
			});},
			get rc () {return __get__ (this, function (self, klass) {
				self.e.classList.remove (klass);
				return self;
			});},
			get arc () {return __get__ (this, function (self, cond, klass) {
				if (cond) {
					self.e.classList.add (klass);
				}
				else {
					self.e.classList.remove (klass);
				}
				return self;
			});},
			get v () {return __get__ (this, function (self) {
				return self.e.value;
			});},
			get focusme () {return __get__ (this, function (self) {
				self.e.focus ();
				return self;
			});},
			get fl () {return __get__ (this, function (self) {
				setTimeout (self.focusme, 50);
				return self;
			});},
			get ae () {return __get__ (this, function (self, kind, callback) {
				self.e.addEventListener (kind, callback);
				return self;
			});},
			get aef () {return __get__ (this, function (self, kind, callback) {
				self.e.addEventListener (kind, callback, false);
				return self;
			});},
			get disable () {return __get__ (this, function (self) {
				return self.sa ('disabled', true);
			});},
			get enable () {return __get__ (this, function (self) {
				return self.ra ('disabled');
			});},
			get able () {return __get__ (this, function (self, able) {
				if (able) {
					return self.enable ();
				}
				return self.disable ();
			});},
			get fs () {return __get__ (this, function (self, size) {
				self.e.style.fontSize = size + 'px';
				return self;
			});}
		});
		var Div = __class__ ('Div', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (Div, '__init__') (self, 'div');
			});}
		});
		var Span = __class__ ('Span', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (Span, '__init__') (self, 'span');
			});}
		});
		var Input = __class__ ('Input', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, kind) {
				__super__ (Input, '__init__') (self, 'input');
				self.sa ('type', kind);
			});}
		});
		var Select = __class__ ('Select', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (Select, '__init__') (self, 'select');
			});}
		});
		var Option = __class__ ('Option', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, key, displayname, selected) {
				if (typeof selected == 'undefined' || (selected != null && selected .hasOwnProperty ("__kwargtrans__"))) {;
					var selected = false;
				};
				__super__ (Option, '__init__') (self, 'option');
				self.sa ('name', key);
				self.sa ('id', key);
				self.sv (key);
				self.html (displayname);
				if (selected) {
					self.sa ('selected', true);
				}
			});}
		});
		var Slider = __class__ ('Slider', [Input], {
			__module__: __name__,
			get setmin () {return __get__ (this, function (self, min) {
				self.sa ('min', min);
				return self;
			});},
			get setmax () {return __get__ (this, function (self, max) {
				self.sa ('max', max);
				return self;
			});},
			get __init__ () {return __get__ (this, function (self) {
				__super__ (Slider, '__init__') (self, 'range');
			});}
		});
		var CheckBox = __class__ ('CheckBox', [Input], {
			__module__: __name__,
			get setchecked () {return __get__ (this, function (self, checked) {
				self.e.checked = checked;
				return self;
			});},
			get getchecked () {return __get__ (this, function (self) {
				return self.e.checked;
			});},
			get __init__ () {return __get__ (this, function (self, checked) {
				if (typeof checked == 'undefined' || (checked != null && checked .hasOwnProperty ("__kwargtrans__"))) {;
					var checked = false;
				};
				__super__ (CheckBox, '__init__') (self, 'checkbox');
				self.setchecked (checked);
			});}
		});
		var TextArea = __class__ ('TextArea', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (TextArea, '__init__') (self, 'textarea');
			});},
			get setText () {return __get__ (this, function (self, content) {
				self.sv (content);
				return self;
			});},
			get getText () {return __get__ (this, function (self) {
				return self.v ();
			});}
		});
		var Canvas = __class__ ('Canvas', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, width, height) {
				__super__ (Canvas, '__init__') (self, 'canvas');
				self.width = width;
				self.height = height;
				self.sa ('width', self.width);
				self.sa ('height', self.height);
				self.ctx = self.e.getContext ('2d');
			});},
			get lineWidth () {return __get__ (this, function (self, linewidth) {
				self.ctx.lineWidth = linewidth;
			});},
			get strokeStyle () {return __get__ (this, function (self, strokestyle) {
				self.ctx.strokeStyle = strokestyle;
			});},
			get fillStyle () {return __get__ (this, function (self, fillstyle) {
				self.ctx.fillStyle = fillstyle;
			});},
			get fillRect () {return __get__ (this, function (self, tlv, brv) {
				self.ctx.fillRect (tlv.x, tlv.y, brv.m (tlv).x, brv.m (tlv).y);
			});},
			get py_clear () {return __get__ (this, function (self) {
				self.ctx.clearRect (0, 0, self.width, self.height);
			});},
			get drawline () {return __get__ (this, function (self, fromv, tov) {
				self.ctx.beginPath ();
				self.ctx.moveTo (fromv.x, fromv.y);
				self.ctx.lineTo (tov.x, tov.y);
				self.ctx.stroke ();
			});}
		});
		var Form = __class__ ('Form', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (Form, '__init__') (self, 'form');
			});}
		});
		var P = __class__ ('P', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (P, '__init__') (self, 'p');
			});}
		});
		var Label = __class__ ('Label', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (Label, '__init__') (self, 'label');
			});}
		});
		var FileInput = __class__ ('FileInput', [Input], {
			__module__: __name__,
			get setmultiple () {return __get__ (this, function (self, multiple) {
				self.srac (multiple, 'multiple', true);
				return self;
			});},
			get getmultiple () {return __get__ (this, function (self) {
				return self.ga ('multiple');
			});},
			get setaccept () {return __get__ (this, function (self, accept) {
				return self.sa ('accept', accept);
			});},
			get getaccept () {return __get__ (this, function (self) {
				return self.ga ('accept');
			});},
			get files () {return __get__ (this, function (self) {
				return self.e.files;
			});},
			get __init__ () {return __get__ (this, function (self) {
				__super__ (FileInput, '__init__') (self, 'file');
			});}
		});
		var WINDOW_SAFETY_MARGIN = 10;
		var Button = __class__ ('Button', [Input], {
			__module__: __name__,
			get clicked () {return __get__ (this, function (self) {
				self.callback (self.key);
			});},
			get __init__ () {return __get__ (this, function (self, caption, callback, key) {
				if (typeof callback == 'undefined' || (callback != null && callback .hasOwnProperty ("__kwargtrans__"))) {;
					var callback = null;
				};
				if (typeof key == 'undefined' || (key != null && key .hasOwnProperty ("__kwargtrans__"))) {;
					var key = null;
				};
				__super__ (Button, '__init__') (self, 'button');
				self.sv (caption);
				if (!(callback === null)) {
					self.callback = callback;
					self.key = key;
					self.ae ('mousedown', self.clicked);
				}
			});}
		});
		var RawTextInput = __class__ ('RawTextInput', [Input], {
			__module__: __name__,
			get keyup () {return __get__ (this, function (self, ev) {
				if (!(self.callback === null)) {
					if (ev.keyCode == 13) {
						if (!(self.entercallback === null)) {
							self.entercallback (self.v ());
						}
					}
					else if (!(self.keycallback === null)) {
						self.keycallback (ev.keyCode, self.v ());
					}
				}
			});},
			get setText () {return __get__ (this, function (self, content) {
				self.sv (content);
				return self;
			});},
			get getText () {return __get__ (this, function (self) {
				return self.v ();
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (RawTextInput, '__init__') (self, 'text');
				self.entercallback = args.py_get ('entercallback', null);
				self.keycallback = args.py_get ('keycallback', null);
				self.cssclass = args.py_get ('tinpclass', 'defaultrawtextinput');
				self.ac (self.cssclass);
				self.ae ('keyup', self.keyup);
			});}
		});
		var TextInputWithButton = __class__ ('TextInputWithButton', [e], {
			__module__: __name__,
			get submitcallback () {return __get__ (this, function (self) {
				if (!(self.onsubmitcallback === null)) {
					var v = self.tinp.v ();
					self.tinp.sv ('');
					self.onsubmitcallback (v);
				}
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (TextInputWithButton, '__init__') (self, 'div');
				var contclass = args.py_get ('contclass', 'textinputcontainer');
				args ['tinpclass'] = args.py_get ('tinpclass', 'textinputtext');
				var sbtnclass = args.py_get ('sbtnclass', 'textinputbutton');
				self.container = Div ().ac (contclass);
				self.onsubmitcallback = args.py_get ('submitcallback', null);
				args ['entercallback'] = self.submitcallback;
				self.tinp = RawTextInput (args);
				self.sbtn = Button ('Submit', self.submitcallback).ac (sbtnclass);
				self.container.aa (list ([self.tinp, self.sbtn]));
				self.a (self.container);
			});},
			get focus () {return __get__ (this, function (self) {
				self.tinp.fl ();
				return self;
			});}
		});
		var LogItem = __class__ ('LogItem', [e], {
			__module__: __name__,
			get equalto () {return __get__ (this, function (self, logitem) {
				return self.content == logitem.content && self.kind == logitem.kind;
			});},
			get getcontent () {return __get__ (this, function (self) {
				if (self.mul == 0) {
					return self.content;
				}
				else {
					return "<span class='logitemcontentmul'>+{}</span> {}".format (self.mul, self.content);
				}
			});},
			get updatecontent () {return __get__ (this, function (self) {
				self.cdiv.html (self.getcontent ());
				return self;
			});},
			get __init__ () {return __get__ (this, function (self, content, kind) {
				if (typeof kind == 'undefined' || (kind != null && kind .hasOwnProperty ("__kwargtrans__"))) {;
					var kind = 'normal';
				};
				__super__ (LogItem, '__init__') (self, 'div');
				self.kind = kind;
				self.mul = 0;
				self.tdiv = Div ().ac ('logtimediv').html ('{}'.format (new Date ().toLocaleTimeString ()));
				self.content = content;
				self.cdiv = Div ().ac ('logcontentdiv');
				if (len (self.content) > 0) {
					if (self.content [0] == '[' || self.content [0] == '{') {
						try {
							var json = JSON.parse (self.content);
							var jsonstr = JSON.stringify (json, null, 2);
							self.content = ('<pre>' + jsonstr) + '</pre>';
							self.cdiv.ac ('logcontentjson');
						}
						catch (__except0__) {
							// pass;
						}
					}
				}
				self.content = striplonglines (self.content);
				if (len (self.content) > MAX_CONTENT_LENGTH) {
					self.content = self.content.__getslice__ (0, MAX_CONTENT_LENGTH, 1);
				}
				self.cdiv.html (self.content);
				if (self.kind == 'cmd') {
					self.cdiv.ac ('logcontentcmd');
				}
				else if (self.kind == 'cmdinfo') {
					self.cdiv.ac ('logcontentcmdinfo');
				}
				else if (self.kind == 'cmdreadline') {
					self.cdiv.ac ('logcontentcmdreadline');
				}
				else if (self.kind == 'cmdstatusok') {
					self.cdiv.ac ('logcontentcmdstatusok');
				}
				else if (self.kind == 'cmdstatuserr') {
					self.cdiv.ac ('logcontentcmdstatuserr');
				}
				self.idiv = Div ().ac ('logitemdiv').aa (list ([self.tdiv, self.cdiv]));
				self.idiv.aa (list ([self.tdiv, self.cdiv]));
				self.a (self.idiv);
			});}
		});
		var Log = __class__ ('Log', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (Log, '__init__') (self, 'div');
				self.width = args.py_get ('width', 600);
				self.height = args.py_get ('height', 400);
				self.maxitems = args.py_get ('maxitems', 100);
				self.ac ('logdiv');
				self.py_items = list ([]);
				self.resize (self.width, self.height);
			});},
			get resize () {return __get__ (this, function (self, width, height) {
				self.width = width;
				self.height = height;
				self.w (self.width).mh (self.height);
				return self;
			});},
			get build () {return __get__ (this, function (self) {
				self.x ();
				var __iterable0__ = py_reversed (self.py_items);
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					item.updatecontent ();
					self.a (item);
				}
			});},
			get add () {return __get__ (this, function (self, item) {
				if (len (self.py_items) > 0) {
					var last = self.py_items [len (self.py_items) - 1];
					if (last.equalto (item)) {
						last.mul++;
					}
					else {
						self.py_items.append (item);
					}
				}
				else {
					self.py_items.append (item);
				}
				if (len (self.py_items) > self.maxitems) {
					self.py_items = self.py_items.__getslice__ (1, null, 1);
				}
			});},
			get log () {return __get__ (this, function (self, item) {
				self.add (item);
				self.build ();
			});}
		});
		var Tab = __class__ ('Tab', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, key, displayname, element) {
				self.key = key;
				self.displayname = displayname;
				self.element = element;
				self.tabelement = null;
			});}
		});
		var TabPane = __class__ ('TabPane', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (TabPane, '__init__') (self, 'div');
				self.id = args.py_get ('id', null);
				self.kind = args.py_get ('kind', 'child');
				self.width = args.py_get ('width', 600);
				self.height = args.py_get ('height', 400);
				self.marginleft = args.py_get ('marginleft', 0);
				self.margintop = args.py_get ('margintop', 0);
				self.tabsheight = args.py_get ('tabsheight', 40);
				self.tabsdiv = Div ().ac ('tabpanetabsdiv');
				self.contentdiv = Div ().ac ('tabpanecontentdiv');
				self.container = Div ().ac ('tabpanecontainer');
				self.container.aa (list ([self.tabsdiv, self.contentdiv]));
				self.a (self.container);
				self.tabs = list ([]);
				self.seltab = null;
				self.resize ();
			});},
			get resize () {return __get__ (this, function (self, width, height) {
				if (typeof width == 'undefined' || (width != null && width .hasOwnProperty ("__kwargtrans__"))) {;
					var width = null;
				};
				if (typeof height == 'undefined' || (height != null && height .hasOwnProperty ("__kwargtrans__"))) {;
					var height = null;
				};
				if (self.kind == 'main') {
					self.width = window.innerWidth - 2 * WINDOW_SAFETY_MARGIN;
					self.height = window.innerHeight - 2 * WINDOW_SAFETY_MARGIN;
					self.marginleft = WINDOW_SAFETY_MARGIN;
					self.margintop = WINDOW_SAFETY_MARGIN;
				}
				if (!(width === null)) {
					self.width = width;
				}
				if (!(height === null)) {
					self.height = height;
				}
				self.contentheight = self.height - self.tabsheight;
				self.tabsdiv.w (self.width).h (self.tabsheight);
				self.contentdiv.w (self.width).h (self.contentheight);
				self.container.w (self.width).h (self.height).ml (self.marginleft).mt (self.margintop);
				try {
					self.resizecontent (self.seltab.element);
				}
				catch (__except0__) {
					// pass;
				}
			});},
			get tabSelectedCallback () {return __get__ (this, function (self, tab) {
				self.selectByKey (tab.key);
			});},
			get setTabs () {return __get__ (this, function (self, tabs, key) {
				self.tabs = tabs;
				self.tabsdiv.x ();
				var __iterable0__ = self.tabs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var tab = __iterable0__ [__index0__];
					var tabelement = Div ().aac (list (['tabpanetab', 'noselect'])).html (tab.displayname);
					self.tabsdiv.a (tabelement);
					tab.tabelement = tabelement;
					tab.tabelement.ae ('mousedown', self.tabSelectedCallback.bind (self, tab));
				}
				if (!(self.key === null)) {
					var storedkey = localStorage.getItem (self.id);
					if (!(storedkey === null)) {
						var key = storedkey;
					}
				}
				return self.selectByKey (key);
			});},
			get getTabByKey () {return __get__ (this, function (self, key, updateclass) {
				if (typeof updateclass == 'undefined' || (updateclass != null && updateclass .hasOwnProperty ("__kwargtrans__"))) {;
					var updateclass = false;
				};
				if (len (self.tabs) == 0) {
					return null;
				}
				var seltab = self.tabs [0];
				var __iterable0__ = self.tabs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var tab = __iterable0__ [__index0__];
					if (updateclass) {
						tab.tabelement.rc ('tabpaneseltab');
						if (tab.key == key) {
							tab.tabelement.ac ('tabpaneseltab');
						}
					}
					if (tab.key == key) {
						var seltab = tab;
					}
				}
				return seltab;
			});},
			get innercontentheight () {return __get__ (this, function (self) {
				return self.contentheight - SCROLL_BAR_WIDTH;
			});},
			get innercontentwidth () {return __get__ (this, function (self) {
				return self.width - SCROLL_BAR_WIDTH;
			});},
			get resizecontent () {return __get__ (this, function (self, element) {
				try {
					element.resize (self.innercontentwidth (), self.innercontentheight ());
				}
				catch (__except0__) {
					// pass;
				}
			});},
			get setTabElementByKey () {return __get__ (this, function (self, key, tabelement) {
				if (typeof tabelement == 'undefined' || (tabelement != null && tabelement .hasOwnProperty ("__kwargtrans__"))) {;
					var tabelement = null;
				};
				var tab = self.getTabByKey (key, tabelement === null);
				if (tab == null) {
					return self;
				}
				if (!(tabelement === null)) {
					tab.element = tabelement;
					if (tab == self.seltab) {
						self.contentdiv.x ().a (tab.element);
					}
				}
				else {
					self.seltab = tab;
					self.contentdiv.x ().a (tab.element);
				}
				self.resizecontent (tab.element);
				return self;
			});},
			get selectByKey () {return __get__ (this, function (self, key) {
				if (!(self.id === null)) {
					localStorage.setItem (self.id, key);
				}
				return self.setTabElementByKey (key);
			});}
		});
		var ComboOption = __class__ ('ComboOption', [object], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, key, displayname) {
				self.key = key;
				self.displayname = displayname;
			});}
		});
		var ComboBox = __class__ ('ComboBox', [e], {
			__module__: __name__,
			get selectchangecallback () {return __get__ (this, function (self) {
				var key = self.select.v ();
				if (!(self.changecallback === null)) {
					self.changecallback (key);
				}
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (ComboBox, '__init__') (self, 'div');
				self.selectclass = args.py_get ('selectclass', 'comboboxselect');
				self.optionfirstclass = args.py_get ('optionfirstclass', 'comboboxoptionfirst');
				self.optionclass = args.py_get ('optionclass', 'comboboxoption');
				self.changecallback = args.py_get ('changecallback', null);
				self.options = list ([]);
				self.container = Div ();
				self.select = Select ().aac (list (['comboboxselect', self.selectclass]));
				self.select.ae ('change', self.selectchangecallback);
				self.container.a (self.select);
				self.a (self.container);
			});},
			get setoptions () {return __get__ (this, function (self, options, selectedkey) {
				if (typeof selectedkey == 'undefined' || (selectedkey != null && selectedkey .hasOwnProperty ("__kwargtrans__"))) {;
					var selectedkey = null;
				};
				self.options = options;
				self.select.x ();
				var first = true;
				var __iterable0__ = self.options.py_items ();
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var __left0__ = __iterable0__ [__index0__];
					var key = __left0__ [0];
					var displayname = __left0__ [1];
					var opte = Option (key, displayname, key == selectedkey);
					if (first) {
						opte.ac (self.optionfirstclass);
						var first = false;
					}
					else {
						opte.ac (self.optionclass);
					}
					self.select.a (opte);
				}
				return self;
			});}
		});
		var LinkedCheckBox = __class__ ('LinkedCheckBox', [Input], {
			__module__: __name__,
			get setchecked () {return __get__ (this, function (self, checked) {
				self.e.checked = checked;
				return self;
			});},
			get getchecked () {return __get__ (this, function (self) {
				return self.e.checked;
			});},
			get updatevar () {return __get__ (this, function (self) {
				self.parent [self.varname] = self.getchecked ();
			});},
			get changed () {return __get__ (this, function (self) {
				self.updatevar ();
				if (!(self.changecallback === null)) {
					self.changecallback ();
				}
			});},
			get __init__ () {return __get__ (this, function (self, parent, varname, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (LinkedCheckBox, '__init__') (self, 'checkbox');
				self.parent = parent;
				self.varname = varname;
				self.setchecked (self.parent [self.varname]);
				self.changecallback = args.py_get ('changecallback', null);
				self.ae ('change', self.changed);
			});}
		});
		var LinkedTextInput = __class__ ('LinkedTextInput', [e], {
			__module__: __name__,
			get updatevar () {return __get__ (this, function (self) {
				self.parent [self.varname] = self.getText ();
			});},
			get keyup () {return __get__ (this, function (self) {
				self.updatevar ();
				if (!(self.keyupcallback === null)) {
					self.keyupcallback ();
				}
			});},
			get setText () {return __get__ (this, function (self, content) {
				self.rawtextinput.setText (content);
				return self;
			});},
			get getText () {return __get__ (this, function (self) {
				return self.rawtextinput.getText ();
			});},
			get able () {return __get__ (this, function (self, enabled) {
				self.rawtextinput.able (enabled);
				return self;
			});},
			get __init__ () {return __get__ (this, function (self, parent, varname, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (LinkedTextInput, '__init__') (self, 'div');
				self.parent = parent;
				self.varname = varname;
				self.value = self.parent [self.varname];
				self.rawtextinputclass = args.py_get ('textclass', 'defaultlinkedtextinputtext');
				self.rawtextinput = RawTextInput (dict ({'keycallback': self.keyup, 'entercallback': self.keyup, 'tinpclass': self.rawtextinputclass}));
				self.setText (self.value);
				patchclasses (self, args);
				self.keyupcallback = args.py_get ('keyupcallback', null);
				self.a (self.rawtextinput);
			});}
		});
		var LinkedSlider = __class__ ('LinkedSlider', [e], {
			__module__: __name__,
			get changed () {return __get__ (this, function (self) {
				self.verify ();
				if (!(self.changecallback === null)) {
					self.changecallback ();
				}
			});},
			get sliderchanged () {return __get__ (this, function (self) {
				if (self.sliderenabled) {
					self.value = self.slider.v ();
					self.valuetextinput.setText (self.value);
					self.verify ();
					if (!(self.changecallback === null)) {
						self.changecallback ();
					}
				}
			});},
			get setslider () {return __get__ (this, function (self) {
				self.sliderenabled = false;
				self.slider.setmin (self.minvalue);
				self.slider.setmax (self.maxvalue);
				self.slider.sv (self.value);
				self.sliderenabled = true;
			});},
			get build () {return __get__ (this, function (self) {
				self.container = Div ().aac (list (['linkedslidercontainerclass', self.containerclass]));
				self.valuetextinput = LinkedTextInput (self, 'value', dict ({'keyupcallback': self.changed, 'textclass': self.valuetextclass}));
				self.mintextinput = LinkedTextInput (self, 'minvalue', dict ({'keyupcallback': self.changed, 'textclass': self.mintextclass}));
				self.maxtextinput = LinkedTextInput (self, 'maxvalue', dict ({'keyupcallback': self.changed, 'textclass': self.maxtextclass}));
				self.slider = Slider ().aac (list (['linkedslidersliderclass', self.sliderclass]));
				self.slider.ae ('change', self.sliderchanged);
				self.container.aa (list ([self.valuetextinput, self.mintextinput, self.slider, self.maxtextinput]));
				self.x ().a (self.container);
				self.verify ();
				return self;
			});},
			get verify () {return __get__ (this, function (self) {
				try {
					self.value = int (self.value);
				}
				catch (__except0__) {
					self.value = 1;
				}
				try {
					self.minvalue = int (self.minvalue);
				}
				catch (__except0__) {
					self.minvalue = 1;
				}
				try {
					self.maxvalue = int (self.maxvalue);
				}
				catch (__except0__) {
					self.maxvalue = 100;
				}
				self.parent [self.varname] = self.value;
				self.parent [self.minvarname] = self.minvalue;
				self.parent [self.maxvarname] = self.maxvalue;
				self.setslider ();
			});},
			get __init__ () {return __get__ (this, function (self, parent, varname, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (LinkedSlider, '__init__') (self, 'div');
				self.parent = parent;
				self.varname = varname;
				self.minvarname = 'min' + self.varname;
				self.maxvarname = 'max' + self.varname;
				self.value = self.parent [self.varname];
				self.minvalue = self.parent [self.minvarname];
				self.maxvalue = self.parent [self.maxvarname];
				self.changecallback = args.py_get ('changecallback', null);
				self.containerclass = args.py_get ('containerclass', 'linkedslidercontainerclass');
				self.valuetextclass = args.py_get ('valuetextclass', 'linkedslidervaluetextclass');
				self.mintextclass = args.py_get ('mintextclass', 'linkedslidermintextclass');
				self.sliderclass = args.py_get ('sliderclass', 'linkedslidersliderclass');
				self.maxtextclass = args.py_get ('maxtextclass', 'linkedslidermaxtextclass');
				self.build ();
			});}
		});
		var LinkedTextarea = __class__ ('LinkedTextarea', [e], {
			__module__: __name__,
			get updatevar () {return __get__ (this, function (self) {
				self.parent [self.varname] = self.getText ();
			});},
			get keyup () {return __get__ (this, function (self) {
				self.updatevar ();
			});},
			get setText () {return __get__ (this, function (self, content) {
				self.textarea.setText (content);
			});},
			get getText () {return __get__ (this, function (self) {
				return self.textarea.getText ();
			});},
			get __init__ () {return __get__ (this, function (self, parent, varname, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (LinkedTextarea, '__init__') (self, 'div');
				self.parent = parent;
				self.varname = varname;
				self.textarea = TextArea ();
				self.textarea.ae ('keyup', self.keyup);
				self.text = args.py_get ('text', '');
				self.setText (self.text);
				patchclasses (self, args);
				self.a (self.textarea);
			});}
		});
		var LabeledLinkedCheckBox = __class__ ('LabeledLinkedCheckBox', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, label, parent, varname, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (LabeledLinkedCheckBox, '__init__') (self, 'div');
				self.lcb = LinkedCheckBox (parent, varname, args);
				self.container = Div ().ac ('labeledlinkedcheckboxcontainer');
				self.ldiv = Div ().html (label);
				self.container.aa (list ([self.ldiv, self.lcb]));
				patchclasses (self, args);
				self.a (self.container).ac ('labeledlinkedcheckbox');
			});}
		});
		var LogPane = __class__ ('LogPane', [e], {
			__module__: __name__,
			get resize () {return __get__ (this, function (self, width, height) {
				self.width = width;
				self.height = height;
				self.contentheight = self.height;
				if (self.contentheight < self.mincontentheight) {
					self.contentheight = self.mincontentheight;
				}
				self.contentdiv.w (self.width).h (self.contentheight);
				self.w (self.width).h (self.height);
				try {
					self.content.resize (self.innercontentwidth (), self.innercontentheight ());
				}
				catch (__except0__) {
					// pass;
				}
			});},
			get innercontentheight () {return __get__ (this, function (self) {
				return self.contentheight - SCROLL_BAR_WIDTH;
			});},
			get innercontentwidth () {return __get__ (this, function (self) {
				return self.width - SCROLL_BAR_WIDTH;
			});},
			get setcontent () {return __get__ (this, function (self, element) {
				self.content = element;
				self.contentdiv.x ().a (self.content);
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (LogPane, '__init__') (self, 'div');
				self.width = args.py_get ('width', 600);
				self.height = args.py_get ('height', 400);
				self.mincontentheight = args.py_get ('mincontentheight', 100);
				self.contentdiv = Div ().ac ('logpanecontentdiv');
				self.resize (self.width, self.height);
				self.aa (list ([self.contentdiv]));
				self.log = Log (dict ({}));
				self.setcontent (self.log);
			});}
		});
		var SplitPane = __class__ ('SplitPane', [e], {
			__module__: __name__,
			get resize () {return __get__ (this, function (self, width, height) {
				self.width = width;
				self.height = height;
				self.controldiv.w (self.width).h (self.controlheight);
				self.contentheight = self.height - self.controlheight;
				if (self.contentheight < self.mincontentheight) {
					self.contentheight = self.mincontentheight;
				}
				self.contentdiv.w (self.width).h (self.contentheight);
				self.w (self.width).h (self.height);
				try {
					self.content.resize (self.innercontentwidth (), self.innercontentheight ());
				}
				catch (__except0__) {
					// pass;
				}
			});},
			get innercontentheight () {return __get__ (this, function (self) {
				return self.contentheight - SCROLL_BAR_WIDTH;
			});},
			get innercontentwidth () {return __get__ (this, function (self) {
				return self.width - SCROLL_BAR_WIDTH;
			});},
			get setcontent () {return __get__ (this, function (self, element) {
				self.content = element;
				self.contentdiv.x ().a (self.content);
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (SplitPane, '__init__') (self, 'div');
				self.width = args.py_get ('width', 600);
				self.height = args.py_get ('height', 400);
				self.controlheight = args.py_get ('controlheight', 100);
				self.mincontentheight = args.py_get ('mincontentheight', 100);
				self.controldiv = Div ().ac ('splitpanecontrolpanel');
				self.contentdiv = Div ().ac ('splitpanecontentdiv');
				self.resize (self.width, self.height);
				self.aa (list ([self.controldiv, self.contentdiv]));
			});}
		});
		var ProcessConsole = __class__ ('ProcessConsole', [SplitPane], {
			__module__: __name__,
			get aliascallback () {return __get__ (this, function (self, key) {
				var cmds = self.cmdaliases [key] ['cmds'];
				var __iterable0__ = cmds;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var cmd = __iterable0__ [__index0__];
					self.submitcallback (cmd);
				}
			});},
			get submitcallback () {return __get__ (this, function (self, content) {
				self.log.log (LogItem (content, 'cmd'));
				if (self.cmdinpcallback === null) {
					return ;
				}
				self.cmdinpcallback (content, self.key);
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				args ['controlheight'] = 80;
				__super__ (ProcessConsole, '__init__') (self, args);
				self.key = args.py_get ('key', null);
				self.cmdinpcallback = args.py_get ('cmdinpcallback', null);
				self.cmdinp = TextInputWithButton (dict ({'submitcallback': self.submitcallback}));
				self.cmdaliases = args.py_get ('cmdaliases', dict ({}));
				self.controldiv.a (self.cmdinp);
				var __iterable0__ = self.cmdaliases.py_keys ();
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var cmdaliaskey = __iterable0__ [__index0__];
					var cmdalias = self.cmdaliases [cmdaliaskey];
					var btn = Button (cmdalias ['display'], self.aliascallback, cmdaliaskey);
					self.controldiv.a (btn);
				}
				self.log = Log (dict ({}));
				self.setcontent (self.log);
			});}
		});
		var FileUploader = __class__ ('FileUploader', [e], {
			__module__: __name__,
			get fileinputchanged () {return __get__ (this, function (self) {
				self.files = self.fileinput.files ();
				self.handlefiles ();
			});},
			get preventdefaults () {return __get__ (this, function (self, ev) {
				ev.preventDefault ();
				ev.stopPropagation ();
			});},
			get highlight () {return __get__ (this, function (self) {
				self.droparea.ac ('highlight');
			});},
			get unhighlight () {return __get__ (this, function (self) {
				self.droparea.rc ('highlight');
			});},
			get log () {return __get__ (this, function (self, html) {
				self.infoitems.append (html);
				self.infoitems.reverse ();
				self.info.html ('<br>'.join (self.infoitems));
				self.infoitems.reverse ();
			});},
			get loginfo () {return __get__ (this, function (self, content) {
				try {
					var json = JSON.parse (content);
					if (json ['success']) {
						var path = '/uploads/{}'.format (json ['savefilename']);
						self.log ("uploaded <span class='fileuploadfilename'>{}</span> <a href='{}' target='_blank' rel='noopener noreferrer'>{}</a>".format (json ['filename'], path, path));
					}
					else {
						self.log ('File upload failed.', json ['status']);
					}
				}
				catch (__except0__) {
					self.log ('Error parsing response as JSON.');
				}
			});},
			get uploadfile () {return __get__ (this, function (self, file) {
				if (self.url === null) {
					print ('no upload url');
					return ;
				}
				var formdata = new FormData ();
				formdata.append ('files', file);
				var args = {'method': 'POST', 'body': formdata};
				fetch (self.url, args).then ((function __lambda__ (response) {
					return response.text ().then ((function __lambda__ (content) {
						return self.loginfo (content);
					}), (function __lambda__ (err) {
						return self.loginfo (err);
					}));
				}), (function __lambda__ (err) {
					return self.loginfo (err);
				}));
			});},
			get handlefiles () {return __get__ (this, function (self, files) {
				if (typeof files == 'undefined' || (files != null && files .hasOwnProperty ("__kwargtrans__"))) {;
					var files = self.files;
				};
				for (var i = 0; i < files.length; i++) {
					print ('uploading file {}'.format (i));
					self.uploadfile (files.item (i));
				}
			});},
			get handledrop () {return __get__ (this, function (self, ev) {
				self.dt = ev.dataTransfer;
				self.files = self.dt.files;
				self.handlefiles ();
			});},
			get build () {return __get__ (this, function (self) {
				self.x ();
				self.droparea = Div ().ac ('fileuploaddroparea');
				self.form = Form ().ac ('fileuploadform');
				self.desc = P ().ac ('fileuploadp').html ('Upload {}s with the file dialog or by dragging and dropping them onto the dashed region'.format (self.acceptdisplay));
				self.fileinput = FileInput ().ac ('fileuploadfileelem').setmultiple (self.multiple).setaccept (self.accept);
				self.fileinput.sa ('id', 'fileinputelement');
				self.fileinput.ae ('change', self.fileinputchanged);
				self.button = Label ().ac ('fileuploadbutton').sa ('for', 'fileinputelement').html ('Select some {}s'.format (self.acceptdisplay));
				self.form.aa (list ([self.desc, self.fileinput, self.button]));
				self.droparea.a (self.form);
				var __iterable0__ = list (['dragenter', 'dragover', 'dragleave', 'drop']);
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var eventname = __iterable0__ [__index0__];
					self.droparea.aef (eventname, self.preventdefaults);
				}
				var __iterable0__ = list (['dragenter', 'dragover']);
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var eventname = __iterable0__ [__index0__];
					self.droparea.aef (eventname, self.highlight);
				}
				var __iterable0__ = list (['dragleave', 'drop']);
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var eventname = __iterable0__ [__index0__];
					self.droparea.aef (eventname, self.unhighlight);
				}
				self.droparea.aef ('drop', self.handledrop);
				self.info = Div ().ac ('fileuploadinfo');
				self.infoitems = list ([]);
				self.aa (list ([self.droparea, self.info]));
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				__super__ (FileUploader, '__init__') (self, 'div');
				self.url = args.py_get ('url', null);
				self.multiple = args.py_get ('multiple', true);
				self.accept = args.py_get ('accept', 'image/*');
				self.acceptdisplay = args.py_get ('acceptdisplay', 'image');
				self.build ();
			});}
		});
		var schemaclipboard = null;
		var SCHEMA_WRITE_PREFERENCE_DEFAULTS = list ([dict ({'key': 'addchild', 'display': 'Add child', 'default': true}), dict ({'key': 'remove', 'display': 'Remove', 'default': true}), dict ({'key': 'childsopened', 'display': 'Childs opened', 'default': false}), dict ({'key': 'editenabled', 'display': 'Edit enabled', 'default': true}), dict ({'key': 'editkey', 'display': 'Edit key', 'default': true}), dict ({'key': 'editvalue', 'display': 'Edit value', 'default': true}), dict ({'key': 'radio', 'display': 'Radio', 'default': false}), dict ({'key': 'slider', 'display': 'Slider', 'default': false}), dict ({'key': 'check', 'display': 'Check', 'default': false}), dict ({'key': 'showhelpashtml', 'display': 'Show help as HTML', 'default': true})]);
		var SchemaWritePreference = __class__ ('SchemaWritePreference', [object], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				var __iterable0__ = SCHEMA_WRITE_PREFERENCE_DEFAULTS;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					self [item ['key']] = item ['default'];
				}
				self.parent = null;
				self.changecallback = null;
				self.disabledlist = list ([]);
			});},
			get setparent () {return __get__ (this, function (self, parent) {
				self.parent = parent;
				return self;
			});},
			get setchangecallback () {return __get__ (this, function (self, changecallback) {
				self.changecallback = changecallback;
				return self;
			});},
			get changed () {return __get__ (this, function (self) {
				if (!(self.changecallback === null)) {
					self.changecallback ();
				}
			});},
			get setdisabledlist () {return __get__ (this, function (self, disabledlist) {
				self.disabledlist = disabledlist;
				return self;
			});},
			get form () {return __get__ (this, function (self) {
				var formdiv = Div ().ac ('noselect');
				var mdl = self.disabledlist;
				if (!(self.parent === null)) {
					if (self.parent.parent === null) {
						var mdl = mdl + list (['editkey']);
					}
				}
				var __iterable0__ = SCHEMA_WRITE_PREFERENCE_DEFAULTS;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					if (!(__in__ (item ['key'], mdl))) {
						formdiv.a (LabeledLinkedCheckBox (item ['display'], self, item ['key'], dict ({'patchclasses': list (['container/a/schemawritepreferenceformsubdiv']), 'changecallback': self.changed})));
					}
				}
				return formdiv;
			});},
			get toobj () {return __get__ (this, function (self) {
				var obj = dict ({});
				var __iterable0__ = SCHEMA_WRITE_PREFERENCE_DEFAULTS;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					obj [item ['key']] = self [item ['key']];
				}
				return obj;
			});}
		});
		var DEFAULT_HELP = 'No help available for this item.';
		var DEFAULT_ENABLED = true;
		var SchemaItem = __class__ ('SchemaItem', [e], {
			__module__: __name__,
			get parentsettask () {return __get__ (this, function (self) {
				// pass;
			});},
			get setparent () {return __get__ (this, function (self, parent) {
				self.parent = parent;
				self.parentsettask ();
			});},
			get getitem () {return __get__ (this, function (self) {
				return self;
			});},
			get label () {return __get__ (this, function (self) {
				return '';
			});},
			get baseobj () {return __get__ (this, function (self) {
				var obj = dict ({'kind': self.kind, 'enabled': self.enabled, 'help': self.help, 'writepreference': self.writepreference.toobj ()});
				return obj;
			});},
			get toobj () {return __get__ (this, function (self) {
				return self.baseobj ();
			});},
			get topureobj () {return __get__ (this, function (self) {
				var pureobj = dict ({});
				return pureobj;
			});},
			get enablechangedtask () {return __get__ (this, function () {
				// pass;
			});},
			get enablecallback () {return __get__ (this, function (self) {
				self.enabled = self.enablecheckbox.getchecked ();
				if (!(self.childparent === null)) {
					if (self.childparent.writepreference.radio) {
						self.childparent.setradio (self);
					}
					self.childparent.enablechangedtask ();
				}
				self.enablechangedtask ();
			});},
			get setenabled () {return __get__ (this, function (self, enabled) {
				self.enabled = enabled;
				self.enablecheckbox.setchecked (self.enabled);
			});},
			get helpboxclicked () {return __get__ (this, function (self) {
				if (self.helpopen) {
					self.helphook.x ();
					self.helpopen = false;
				}
				else {
					self.helpdiv = Div ().ac ('schemahelpdiv');
					self.helpcontentdiv = Div ().aac (list (['schemahelpcontentdiv', 'noselect'])).html (self.help);
					self.helpeditdiv = Div ().ac ('schemahelpeditdiv');
					self.helpedittextarea = LinkedTextarea (self, 'help', dict ({'patchclasses': list (['textarea/a/schemahelpedittextarea']), 'text': self.help}));
					self.helpeditdiv.a (self.helpedittextarea);
					if (self.writepreference.showhelpashtml) {
						self.helpdiv.a (self.helpcontentdiv);
					}
					else {
						self.helpdiv.a (self.helpeditdiv);
					}
					self.helphook.a (self.helpdiv);
					self.helpopen = true;
				}
			});},
			get copyboxclicked () {return __get__ (this, function (self) {
				schemaclipboard.copy (self);
			});},
			get settingsboxclicked () {return __get__ (this, function (self) {
				if (self.settingsopen) {
					self.settingshook.x ();
					self.settingsopen = false;
				}
				else {
					self.settingsdiv = Div ().ac ('schemasettingsdiv').a (self.writepreference.form ());
					self.settingshook.a (self.settingsdiv);
					self.settingsopen = true;
				}
			});},
			get removeboxclicked () {return __get__ (this, function (self) {
				self.childparent.remove (self);
				// pass;
			});},
			get writepreferencechangedtask () {return __get__ (this, function (self) {
				// pass;
			});},
			get writepreferencechanged () {return __get__ (this, function (self) {
				self.helpboxclicked ();
				self.helpboxclicked ();
				self.enablecheckbox.able (self.writepreference.editenabled);
				self.setchildparent (self.childparent);
				self.writepreferencechangedtask ();
				if (!(self.parent === null)) {
					self.parent.writepreferencechangedtask ();
				}
			});},
			get setchildparent () {return __get__ (this, function (self, childparent) {
				self.childparent = childparent;
				if (!(self.childparent === null) && self.writepreference.remove) {
					self.schemacontainer.x ().aa (list ([self.enablebox, self.element, self.helpbox, self.copybox, self.settingsbox, self.removebox]));
				}
				else {
					self.schemacontainer.x ().aa (list ([self.enablebox, self.element, self.helpbox, self.copybox, self.settingsbox]));
				}
			});},
			get elementdragstart () {return __get__ (this, function (self, ev) {
				self.dragstartvect = getClientVect (ev);
			});},
			get elementdrag () {return __get__ (this, function (self, ev) {
				// pass;
			});},
			get move () {return __get__ (this, function (self, dir) {
				if (self.childparent === null) {
					return ;
				}
				var i = self.childparent.getitemindex (self);
				var newi = i + dir;
				self.childparent.movechildi (i, newi);
			});},
			get elementdragend () {return __get__ (this, function (self, ev) {
				self.dragendvect = getClientVect (ev);
				var diff = self.dragendvect.m (self.dragstartvect);
				var dir = int (diff.y / getglobalcssvarpxint ('--schemabase'));
				self.move (dir);
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (SchemaItem, '__init__') (self, 'div');
				self.parent = null;
				self.childparent = null;
				self.args = args;
				self.kind = 'item';
				self.enabled = args.py_get ('enabled', DEFAULT_ENABLED);
				self.help = args.py_get ('help', DEFAULT_HELP);
				self.writepreference = args.py_get ('writepreference', SchemaWritePreference ());
				self.writepreference.setparent (self);
				self.writepreference.setchangecallback (self.writepreferencechanged);
				self.element = Div ().ac ('schemaitem');
				self.schemacontainer = Div ().ac ('schemacontainer');
				self.enablebox = Div ().ac ('schemaenablebox');
				self.enablecheckbox = CheckBox (self.enabled).ac ('schemaenablecheckbox').ae ('change', self.enablecallback);
				self.enablecheckbox.able (self.writepreference.editenabled);
				self.enablebox.a (self.enablecheckbox);
				self.helpbox = Div ().aac (list (['schemahelpbox', 'noselect'])).ae ('mousedown', self.helpboxclicked).html ('?');
				self.copybox = Div ().aac (list (['schemacopybox', 'noselect'])).ae ('mousedown', self.copyboxclicked).html ('C');
				self.settingsbox = Div ().aac (list (['schemasettingsbox', 'noselect'])).ae ('mousedown', self.settingsboxclicked).html ('S');
				self.removebox = Div ().aac (list (['schemaremovebox', 'noselect'])).ae ('mousedown', self.removeboxclicked).html ('X');
				self.afterelementhook = Div ();
				self.settingsopen = args.py_get ('settingsopen', false);
				self.helpopen = args.py_get ('helpopen', false);
				self.settingshook = Div ();
				self.helphook = Div ();
				self.schemacontainer.aa (list ([self.enablebox, self.element, self.helpbox, self.copybox, self.settingsbox]));
				self.itemcontainer = Div ();
				self.itemcontainer.aa (list ([self.schemacontainer, self.helphook, self.settingshook, self.afterelementhook]));
				self.a (self.itemcontainer);
				self.dragelement = self.copybox;
				self.dragelement.sa ('draggable', true);
				self.dragelement.ae ('dragstart', self.elementdragstart);
				self.dragelement.ae ('drag', self.elementdrag);
				self.dragelement.ae ('dragend', self.elementdragend);
				self.dragelement.ae ('dragover', (function __lambda__ (ev) {
					return ev.preventDefault ();
				}));
			});}
		});
		var NamedSchemaItem = __class__ ('NamedSchemaItem', [e], {
			__module__: __name__,
			get getitem () {return __get__ (this, function (self) {
				return self.item;
			});},
			get label () {return __get__ (this, function (self) {
				return self.key;
			});},
			get toobj () {return __get__ (this, function (self) {
				return dict ({'kind': 'nameditem', 'key': self.key, 'item': self.item.toobj ()});
			});},
			get writepreferencechangedtask () {return __get__ (this, function (self) {
				self.linkedtextinput.able (self.item.writepreference.editkey);
			});},
			get keychanged () {return __get__ (this, function (self) {
				if (!(self.keychangedcallback === null)) {
					self.keychangedcallback ();
				}
			});},
			get setkeychangedcallback () {return __get__ (this, function (self, keychangedcallback) {
				self.keychangedcallback = keychangedcallback;
				return self;
			});},
			get setkey () {return __get__ (this, function (self, key) {
				self.key = key;
				self.linkedtextinput.setText (self.key);
				return self;
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (NamedSchemaItem, '__init__') (self, 'div');
				self.kind = 'nameditem';
				self.key = args.py_get ('key', '');
				self.item = args.py_get ('item', SchemaItem (args));
				self.keychangedcallback = null;
				self.item.setparent (self);
				self.namedcontainer = Div ().ac ('namedschemaitem');
				self.namediv = Div ().ac ('schemaitemname');
				self.linkedtextinput = LinkedTextInput (self, 'key', dict ({'textclass': 'namedschemaitemrawtextinput', 'keyupcallback': self.keychanged}));
				self.linkedtextinput.setText (self.key);
				self.linkedtextinput.able (self.item.writepreference.editkey);
				self.namediv.a (self.linkedtextinput);
				self.namedcontainer.aa (list ([self.namediv, self.item]));
				self.a (self.namedcontainer);
			});},
			get copy () {return __get__ (this, function (self, item) {
				self.item = schemafromobj (item.toobj ());
				self.item.parent = null;
				self.key = null;
				if (!(item.parent === null)) {
					self.key = item.parent.key;
				}
			});}
		});
		var SchemaScalar = __class__ ('SchemaScalar', [SchemaItem], {
			__module__: __name__,
			get label () {return __get__ (this, function (self) {
				return self.value;
			});},
			get toobj () {return __get__ (this, function (self) {
				var obj = self.baseobj ();
				obj ['value'] = self.value;
				obj ['minvalue'] = self.minvalue;
				obj ['maxvalue'] = self.maxvalue;
				return obj;
			});},
			get topureobj () {return __get__ (this, function (self) {
				var obj = self.value;
				return obj;
			});},
			get writepreferencechangedtask () {return __get__ (this, function (self) {
				self.build ();
			});},
			get enablechangedtask () {return __get__ (this, function (self) {
				if (self.writepreference.check) {
					if (self.enabled) {
						self.value = 'true';
					}
					else {
						self.value = 'false';
					}
					self.linkedtextinput.setText (self.value);
				}
			});},
			get build () {return __get__ (this, function (self) {
				if (self.writepreference.slider) {
					self.enablecheckbox.rc ('schemacheckenablecheckbox');
					self.linkedslider = LinkedSlider (self, 'value', dict ({'containerclass': 'schemalinkedslidercontainerclass', 'valuetextclass': 'schemalinkedslidervaluetextclass', 'mintextclass': 'schemalinkedslidermintextclass', 'sliderclass': 'schemalinkedslidersliderclass', 'maxtextclass': 'schemalinkedslidermaxtextclass'}));
					self.element.x ().aa (list ([self.linkedslider]));
				}
				else {
					self.enablebox.arc (self.writepreference.check, 'schemacheckenablecheckbox');
					self.linkedtextinput = LinkedTextInput (self, 'value', dict ({'textclass': 'schemascalarrawtextinput'}));
					self.linkedtextinput.able (self.writepreference.editvalue);
					self.element.x ().aa (list ([self.linkedtextinput]));
				}
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (SchemaScalar, '__init__') (self, args);
				self.kind = 'scalar';
				self.value = args.py_get ('value', '');
				self.minvalue = args.py_get ('minvalue', 1);
				self.maxvalue = args.py_get ('maxvalue', 100);
				self.element.ac ('schemascalar');
				self.writepreference.setdisabledlist (list (['addchild', 'childsopened', 'radio']));
				self.build ();
			});}
		});
		var SchemaCollection = __class__ ('SchemaCollection', [SchemaItem], {
			__module__: __name__,
			get removechildi () {return __get__ (this, function (self, i) {
				var newchilds = list ([]);
				var rchild = null;
				for (var j = 0; j < len (self.childs); j++) {
					if (j == i) {
						var rchild = self.childs [j];
					}
					else {
						newchilds.append (self.childs [j]);
					}
				}
				self.childs = newchilds;
				self.openchilds ();
				self.openchilds ();
				return rchild;
			});},
			get insertchildi () {return __get__ (this, function (self, i, child) {
				var newchilds = list ([]);
				for (var j = 0; j < len (self.childs) + 1; j++) {
					if (j == i) {
						newchilds.append (child);
					}
					if (j < len (self.childs)) {
						newchilds.append (self.childs [j]);
					}
				}
				self.childs = newchilds;
				self.openchilds ();
				self.openchilds ();
			});},
			get movechildi () {return __get__ (this, function (self, i, newi) {
				if (len (self.childs) <= 0) {
					return ;
				}
				if (newi < 0) {
					var newi = 0;
				}
				if (newi >= len (self.childs)) {
					var newi = len (self.childs) - 1;
				}
				var rchild = self.removechildi (i);
				if (!(rchild === null)) {
					self.insertchildi (newi, rchild);
				}
			});},
			get getitemindex () {return __get__ (this, function (self, item) {
				for (var i = 0; i < len (self.childs); i++) {
					if (self.childs [i].getitem () == item) {
						return i;
					}
				}
				return null;
			});},
			get parentsettask () {return __get__ (this, function (self) {
				self.opendiv.arc (!(self.parent === null), 'schemadictchildleftmargin');
			});},
			get enablechangedtask () {return __get__ (this, function (self) {
				self.openchilds ();
				self.openchilds ();
			});},
			get buildchilds () {return __get__ (this, function (self) {
				var labellist = list ([]);
				self.childshook.x ();
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var child = __iterable0__ [__index0__];
					self.childshook.a (child);
					if (child.getitem ().enabled) {
						labellist.append (child.label ());
					}
				}
				var label = ' , '.join (labellist);
				self.openbutton.x ().a (Div ().ac ('schemacollectionopenbuttonlabel').html (label));
			});},
			get topureobj () {return __get__ (this, function (self) {
				var pureobj = dict ({});
				if (self.writepreference.radio) {
					if (self.kind == 'dict') {
						var pureobj = list (['', dict ({})]);
						var __iterable0__ = self.childs;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var nameditem = __iterable0__ [__index0__];
							var key = nameditem.key;
							var item = nameditem.item;
							if (item.enabled || item.writepreference.check) {
								var pureobj = list ([key, item.topureobj ()]);
								break;
							}
						}
					}
					else if (self.kind == 'list') {
						var __iterable0__ = self.childs;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var item = __iterable0__ [__index0__];
							if (item.enabled || item.writepreference.check) {
								var pureobj = item.topureobj ();
								break;
							}
						}
					}
				}
				else if (self.kind == 'dict') {
					var __iterable0__ = self.childs;
					for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
						var nameditem = __iterable0__ [__index0__];
						var key = nameditem.key;
						var item = nameditem.item;
						if (item.enabled || item.writepreference.check) {
							pureobj [key] = item.topureobj ();
						}
					}
				}
				else if (self.kind == 'list') {
					var pureobj = list ([]);
					var __iterable0__ = self.childs;
					for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
						var item = __iterable0__ [__index0__];
						if (item.enabled || item.writepreference.check) {
							pureobj.append (item.topureobj ());
						}
					}
				}
				return pureobj;
			});},
			get setradio () {return __get__ (this, function (self, item) {
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var child = __iterable0__ [__index0__];
					var childitem = child.getitem ();
					var childeq = childitem == item;
					childitem.enabled = childeq;
					childitem.enablecheckbox.setchecked (childeq);
				}
			});},
			get remove () {return __get__ (this, function (self, item) {
				var newlist = list ([]);
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var child = __iterable0__ [__index0__];
					var childeq = false;
					if (child.kind == 'nameditem') {
						var childeq = child.item == item;
					}
					else {
						var childeq = child == item;
					}
					if (!(childeq)) {
						newlist.append (child);
					}
				}
				self.childs = newlist;
				self.openchilds ();
				self.openchilds ();
			});},
			get getschemakinds () {return __get__ (this, function (self) {
				var schemakinds = dict ({'create': 'Create new', 'scalar': 'Scalar', 'list': 'List', 'dict': 'Dict'});
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var nameditem = __iterable0__ [__index0__];
					var key = nameditem.key;
					if (!(key == null)) {
						if (len (key) > 0) {
							schemakinds ['#' + key] = key;
						}
					}
				}
				return schemakinds;
			});},
			get updatecreatecombo () {return __get__ (this, function (self) {
				if (!(self.createcombo === null)) {
					self.createcombo.setoptions (self.getschemakinds ());
				}
			});},
			get getchildbykey () {return __get__ (this, function (self, key) {
				if (!(self.kind == 'dict')) {
					return null;
				}
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var nameditem = __iterable0__ [__index0__];
					if (nameditem.key == key) {
						return nameditem.item;
					}
				}
				return null;
			});},
			get createcallback () {return __get__ (this, function (self, key) {
				self.updatecreatecombo ();
				var sch = SchemaScalar (dict ({}));
				if (key == 'list') {
					var sch = SchemaList (dict ({}));
				}
				else if (key == 'dict') {
					var sch = SchemaDict (dict ({}));
				}
				if (key [0] == '#') {
					var truekey = key.__getslice__ (1, null, 1);
					var titem = self.getchildbykey (truekey);
					if (titem == null) {
						print ('error, no item with key', truekey);
					}
					else {
						var sch = schemafromobj (titem.toobj ());
					}
				}
				sch.setchildparent (self);
				var appendelement = sch;
				if (self.kind == 'dict') {
					var appendelement = NamedSchemaItem (dict ({'item': sch})).setkeychangedcallback (self.updatecreatecombo);
				}
				self.childs.append (appendelement);
				self.buildchilds ();
				self.updatecreatecombo ();
			});},
			get pastebuttonclicked () {return __get__ (this, function (self) {
				try {
					var sch = schemafromobj (schemaclipboard.item.toobj ());
				}
				catch (__except0__) {
					window.alert ('No item on clipboard to paste!');
					return self;
				}
				sch.setchildparent (self);
				var appendelement = sch;
				if (self.kind == 'dict') {
					var appendelement = NamedSchemaItem (dict ({'item': sch})).setkeychangedcallback (self.updatecreatecombo);
					if (!(schemaclipboard.key === null)) {
						appendelement.setkey (schemaclipboard.key);
					}
				}
				self.childs.append (appendelement);
				self.buildchilds ();
				self.updatecreatecombo ();
			});},
			get openchilds () {return __get__ (this, function (self) {
				if (self.opened) {
					self.opened = false;
					self.createhook.x ();
					self.childshook.x ();
					self.openbutton.rc ('schemacollectionopenbuttondone');
				}
				else {
					self.opened = true;
					self.creatediv = Div ().ac ('schemaitem').ac ('schemacreate');
					self.createcombo = ComboBox (dict ({'changecallback': self.createcallback, 'selectclass': 'schemacreatecomboselect'}));
					self.updatecreatecombo ();
					self.pastebutton = Button ('Paste', self.pastebuttonclicked).ac ('schemapastebutton');
					self.creatediv.aa (list ([self.createcombo, self.pastebutton]));
					if (self.writepreference.addchild) {
						self.createhook.a (self.creatediv);
					}
					self.openbutton.ac ('schemacollectionopenbuttondone');
					self.buildchilds ();
				}
			});},
			get writepreferencechangedtask () {return __get__ (this, function (self) {
				self.openchilds ();
				self.openchilds ();
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (SchemaCollection, '__init__') (self, args);
				self.kind = 'collection';
				self.opened = false;
				self.childs = args.py_get ('childs', list ([]));
				self.editmode = args.py_get ('editmode', false);
				self.childseditable = args.py_get ('childseditable', true);
				self.element.ac ('schemacollection');
				self.openbutton = Div ().aac (list (['schemacollectionopenbutton', 'noselect'])).ae ('mousedown', self.openchilds);
				self.element.aa (list ([self.openbutton]));
				self.createcombo = null;
				self.createhook = Div ();
				self.childshook = Div ();
				self.opendiv = Div ().ac ('schemacollectionopendiv');
				self.opendiv.aa (list ([self.createhook, self.childshook]));
				self.afterelementhook.a (self.opendiv);
				self.openchilds ();
				if (!(self.writepreference.childsopened)) {
					self.openchilds ();
				}
			});}
		});
		var SchemaList = __class__ ('SchemaList', [SchemaCollection], {
			__module__: __name__,
			get getfirstselectedindex () {return __get__ (this, function (self) {
				var i = 0;
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					if (item.enabled) {
						return i;
					}
					i++;
				}
				return null;
			});},
			get toobj () {return __get__ (this, function (self) {
				var listobj = list ([]);
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					listobj.append (item.toobj ());
				}
				var obj = self.baseobj ();
				obj ['items'] = listobj;
				return obj;
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (SchemaList, '__init__') (self, args);
				self.kind = 'list';
				self.element.ac ('schemalist');
				self.writepreference.setdisabledlist (list (['editvalue', 'slider', 'check']));
			});}
		});
		var SchemaDict = __class__ ('SchemaDict', [SchemaCollection], {
			__module__: __name__,
			get setchildatkey () {return __get__ (this, function (self, key, item) {
				item.setchildparent (self);
				var nameditem = NamedSchemaItem (dict ({'key': key, 'item': item}));
				var i = self.getitemindexbykey (key);
				if (i === null) {
					self.childs.append (nameditem);
				}
				else {
					self.childs [i] = nameditem;
				}
				self.openchilds ();
				self.openchilds ();
			});},
			get getfirstselectedindex () {return __get__ (this, function (self) {
				var i = 0;
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					if (item.item.enabled) {
						return i;
					}
					i++;
				}
				return null;
			});},
			get getitemindexbykey () {return __get__ (this, function (self, key) {
				var i = 0;
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					if (item.key == key) {
						return i;
					}
					i++;
				}
				return null;
			});},
			get toobj () {return __get__ (this, function (self) {
				var dictobj = list ([]);
				var __iterable0__ = self.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					var sch = dict ({'key': item.key, 'item': item.item.toobj ()});
					dictobj.append (sch);
				}
				var obj = self.baseobj ();
				obj ['items'] = dictobj;
				return obj;
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (SchemaDict, '__init__') (self, args);
				self.kind = 'dict';
				self.element.ac ('schemadict');
				self.writepreference.setdisabledlist (list (['editvalue', 'slider', 'check']));
			});}
		});
		var schemawritepreferencefromobj = function (obj) {
			var swp = SchemaWritePreference ();
			var __iterable0__ = SCHEMA_WRITE_PREFERENCE_DEFAULTS;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var item = __iterable0__ [__index0__];
				swp [item ['key']] = getfromobj (obj, item ['key'], item ['default']);
			}
			return swp;
		};
		var schemafromobj = function (obj) {
			var kind = getfromobj (obj, 'kind', 'dict');
			var enabled = getfromobj (obj, 'enabled', DEFAULT_ENABLED);
			var help = getfromobj (obj, 'help', DEFAULT_HELP);
			var writepreference = schemawritepreferencefromobj (getfromobj (obj, 'writepreference', dict ({})));
			var returnobj = dict ({});
			if (kind == 'scalar') {
				var returnobj = SchemaScalar (dict ({'value': obj ['value'], 'minvalue': obj ['minvalue'], 'maxvalue': obj ['maxvalue'], 'writepreference': writepreference}));
			}
			else if (kind == 'list') {
				var py_items = obj ['items'];
				var childs = list ([]);
				var __iterable0__ = py_items;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					var sch = schemafromobj (item);
					childs.append (sch);
				}
				var returnobj = SchemaList (dict ({'childs': childs, 'writepreference': writepreference}));
				var __iterable0__ = returnobj.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var child = __iterable0__ [__index0__];
					child.setchildparent (returnobj);
				}
			}
			else if (kind == 'dict') {
				var py_items = obj ['items'];
				var childs = list ([]);
				var __iterable0__ = py_items;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var itemobj = __iterable0__ [__index0__];
					var key = itemobj ['key'];
					var item = itemobj ['item'];
					var sch = schemafromobj (item);
					var namedsch = NamedSchemaItem (dict ({'key': key, 'item': sch, 'writepreference': writepreference}));
					childs.append (namedsch);
				}
				var returnobj = SchemaDict (dict ({'childs': childs, 'writepreference': writepreference}));
				var __iterable0__ = returnobj.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var child = __iterable0__ [__index0__];
					child.item.setchildparent (returnobj);
					child.setkeychangedcallback (returnobj.updatecreatecombo);
				}
			}
			returnobj.setenabled (enabled);
			returnobj.help = help;
			return returnobj;
		};
		var getpathlistfromschema = function (sch, pathlist) {
			if (len (pathlist) <= 0) {
				return sch;
			}
			var key = pathlist [0];
			var pathlist = pathlist.__getslice__ (1, null, 1);
			if (key == '#') {
				if (sch.kind == 'scalar') {
					return null;
				}
				else if (sch.kind == 'list') {
					var i = sch.getfirstselectedindex ();
					if (i == null) {
						return null;
					}
					return getpathlistfromschema (sch.childs [i], pathlist);
				}
				else if (sch.kind == 'dict') {
					var i = sch.getfirstselectedindex ();
					if (i == null) {
						return null;
					}
					return getpathlistfromschema (sch.childs [i].item, pathlist);
				}
			}
			else if (sch.kind == 'scalar') {
				return null;
			}
			else if (sch.kind == 'list') {
				return null;
			}
			else if (sch.kind == 'dict') {
				var __iterable0__ = sch.childs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var child = __iterable0__ [__index0__];
					if (child.key == key) {
						return getpathlistfromschema (child.item, pathlist);
					}
				}
			}
			return null;
		};
		var getpathfromschema = function (sch, path) {
			var pathlist = path.py_split ('/');
			return getpathlistfromschema (sch, pathlist);
		};
		var getscalarfromschema = function (sch, path) {
			var found = getpathfromschema (sch, path);
			if (!(found === null)) {
				if (found.kind == 'scalar') {
					return found.value;
				}
			}
			var found = getpathfromschema (sch, path + '/#');
			if (!(found === null)) {
				if (found.kind == 'scalar') {
					return found.value;
				}
			}
			return null;
		};
		var schemafromucioptionsobj = function (obj) {
			var ucioptions = SchemaDict (dict ({}));
			var __iterable0__ = obj;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var opt = __iterable0__ [__index0__];
				var key = opt ['key'];
				var kind = opt ['kind'];
				var py_default = opt ['default'];
				var min = opt ['min'];
				var max = opt ['max'];
				var options = opt ['options'];
				var item = SchemaScalar (dict ({'value': py_default}));
				if (kind == 'spin') {
					item.minvalue = min;
					item.maxvalue = max;
					item.writepreference.slider = true;
					item.build ();
				}
				else if (kind == 'check') {
					item.value = 'false';
					if (py_default) {
						item.value = 'true';
					}
					item.writepreference.check = true;
					item.setenabled (py_default);
					item.build ();
				}
				else if (kind == 'combo') {
					var item = SchemaList (dict ({}));
					item.writepreference.radio = true;
					var __iterable1__ = options;
					for (var __index1__ = 0; __index1__ < len (__iterable1__); __index1__++) {
						var comboopt = __iterable1__ [__index1__];
						var comboitem = SchemaScalar (dict ({'value': comboopt}));
						comboitem.setenabled (comboopt == py_default);
						comboitem.setchildparent (item);
						item.childs.append (comboitem);
					}
					item.openchilds ();
					item.openchilds ();
				}
				item.setchildparent (ucioptions);
				var nameditem = NamedSchemaItem (dict ({'key': key, 'item': item}));
				ucioptions.childs.append (nameditem);
			}
			return ucioptions;
		};
		var schemaclipboard = NamedSchemaItem (dict ({}));
		var DirBrowser = __class__ ('DirBrowser', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (DirBrowser, '__init__') (self, 'div');
				self.pathlist = list ([]);
				self.loadpathlist (self.pathlist);
			});},
			get loadpathlist () {return __get__ (this, function (self) {
				getjson ('/dirlist/root/{}'.format (self.path ()), self.build, (function __lambda__ (err) {
					return print (err);
				}));
			});},
			get toparentdir () {return __get__ (this, function (self) {
				if (len (self.pathlist) > 0) {
					self.pathlist.py_pop ();
				}
				self.loadpathlist ();
			});},
			get opendirfactory () {return __get__ (this, function (self, py_name) {
				var opendir = function () {
					self.pathlist.append (py_name);
					self.loadpathlist ();
				};
				return opendir;
			});},
			get path () {return __get__ (this, function (self) {
				return '/'.join (self.pathlist);
			});},
			get namepath () {return __get__ (this, function (self, py_name) {
				if (len (self.pathlist) <= 0) {
					return py_name;
				}
				return '/'.join (list ([self.path (), py_name]));
			});},
			get refresh () {return __get__ (this, function (self) {
				self.loadpathlist ();
			});},
			get build () {return __get__ (this, function (self, statsobj) {
				self.x ();
				self.a (Button ('Refresh', self.refresh).ac ('dirbrowserrefreshbutton'));
				var dirs = list ([]);
				var files = list ([]);
				var __iterable0__ = statsobj;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					if (item ['isdir']) {
						dirs.append (item);
					}
					else {
						files.append (item);
					}
				}
				var sorteddirs = sorted (dirs, __kwargtrans__ ({key: (function __lambda__ (item) {
					return item ['name'].toLowerCase ();
				})}));
				var sortedfiles = sorted (files, __kwargtrans__ ({key: (function __lambda__ (item) {
					return item ['name'].toLowerCase ();
				})}));
				var sortedobj = list ([]);
				var __iterable0__ = sorteddirs;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					sortedobj.append (item);
				}
				var __iterable0__ = sortedfiles;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					sortedobj.append (item);
				}
				if (len (self.pathlist) > 0) {
					var updiv = Div ().aac (list (['dirbrowseritem', 'dirbrowserdir', 'noselect'])).ae ('mousedown', self.toparentdir);
					updiv.a (Div ().aac (list (['dirbrowsertoparent', 'dirbrowserdirname'])).html ('..'));
					self.a (updiv);
				}
				var __iterable0__ = sortedobj;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var item = __iterable0__ [__index0__];
					var itemdiv = Div ().aac (list (['dirbrowseritem', 'noselect']));
					var namediv = Div ().ac ('dirbrowsername');
					var sizediv = Div ().ac ('dirbrowsersize');
					if (item ['isdir']) {
						var text = item ['name'];
						itemdiv.ac ('dirbrowserdir').ae ('mousedown', self.opendirfactory (item ['name']));
						namediv.ac ('dirbrowserdirname').html (text);
						sizediv.html ('dir');
					}
					else {
						var text = "<a href='/file/{}' target='_blank' rel='noopener noreferrer'>{}</a>".format (self.namepath (item ['name']), item ['name']);
						itemdiv.ac ('dirbrowserfile');
						namediv.html (text);
						sizediv.html ('{} bytes'.format (item ['st_size']));
					}
					itemdiv.a (namediv);
					itemdiv.a (Div ().ac ('dirbrowsermodat').html (new Date (item ['st_mtime'] * 1000).toLocaleString ()));
					itemdiv.a (sizediv);
					var rwxdiv = Div ().ac ('dirbrowserrwx').html (item ['st_mode_unix_rwx']);
					itemdiv.a (rwxdiv);
					self.a (itemdiv);
				}
			});}
		});
		var STANDARD_START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
		var ANTICHESS_START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1';
		var RACING_KINGS_START_FEN = '8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w - - 0 1';
		var HORDE_START_FEN = 'rnbqkbnr/pppppppp/8/1PP2PP1/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP w kq - 0 1';
		var THREE_CHECK_START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 3+3 0 1';
		var CRAZYHOUSE_START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR[] w KQkq - 0 1';
		var PIECE_KINDS = list (['p', 'n', 'b', 'r', 'q', 'k']);
		var WHITE = 1;
		var BLACK = 0;
		var VARIANT_OPTIONS = dict ({'standard': 'Standard', 'fromPosition': 'From Position', 'antichess': 'Antichess', 'atomic': 'Atomic', 'chess960': 'Chess960', 'crazyhouse': 'Crazyhouse', 'horde': 'Horde', 'kingOfTheHill': 'King of the Hill', 'racingKings': 'Racing Kings', 'threeCheck': 'Three Check'});
		var PIECE_NAMES = dict ({'p': 'Pawn', 'n': 'Knight', 'b': 'Bishop', 'r': 'Rook', 'q': 'Queen', 'k': 'King'});
		var PROMPIECEKINDS_STANDARD = list (['n', 'b', 'r', 'q']);
		var PROMPIECEKINDS_ANTICHESS = list (['n', 'b', 'r', 'q', 'k']);
		var prompiecekindsforvariantkey = function (variantkey) {
			if (variantkey == 'antichess') {
				return PROMPIECEKINDS_ANTICHESS;
			}
			return PROMPIECEKINDS_STANDARD;
		};
		var piececolortocolorname = function (color) {
			if (color == WHITE) {
				return 'White';
			}
			else if (color == BLACK) {
				return 'Black';
			}
			return 'Invalidcolor';
		};
		var piecekindtopiecename = function (kind) {
			if (__in__ (kind, PIECE_NAMES)) {
				return PIECE_NAMES [kind];
			}
			return 'Invalidpiece';
		};
		var getstartfenforvariantkey = function (variantkey) {
			if (variantkey == 'antichess') {
				return ANTICHESS_START_FEN;
			}
			if (variantkey == 'racingKings') {
				return RACING_KINGS_START_FEN;
			}
			if (variantkey == 'horde') {
				return HORDE_START_FEN;
			}
			if (variantkey == 'threeCheck') {
				return THREE_CHECK_START_FEN;
			}
			if (variantkey == 'crazyhouse') {
				return CRAZYHOUSE_START_FEN;
			}
			return STANDARD_START_FEN;
		};
		var Piece = __class__ ('Piece', [object], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, kind, color) {
				if (typeof kind == 'undefined' || (kind != null && kind .hasOwnProperty ("__kwargtrans__"))) {;
					var kind = null;
				};
				if (typeof color == 'undefined' || (color != null && color .hasOwnProperty ("__kwargtrans__"))) {;
					var color = null;
				};
				self.kind = kind;
				self.color = color;
			});},
			get isempty () {return __get__ (this, function (self) {
				return self.kind === null;
			});},
			get ispiece () {return __get__ (this, function (self) {
				return !(self.isempty ());
			});},
			get __repr__ () {return __get__ (this, function (self) {
				if (self.isempty ()) {
					return 'Piece[None]';
				}
				return 'Piece[{} {}]'.format (piececolortocolorname (self.color), piecekindtopiecename (self.kind));
			});}
		});
		var isvalidpieceletter = function (pieceletter) {
			if (__in__ (pieceletter, PIECE_KINDS)) {
				return true;
			}
			if (__in__ (pieceletter.toLowerCase (), PIECE_KINDS)) {
				return true;
			}
			return false;
		};
		var piecelettertopiece = function (pieceletter) {
			if (isvalidpieceletter (pieceletter)) {
				var pieceletterlower = pieceletter.toLowerCase ();
				if (pieceletterlower == pieceletter) {
					return Piece (pieceletterlower, BLACK);
				}
				return Piece (pieceletterlower, WHITE);
			}
			print ('warning, piece letter not valid', pieceletter);
			return Piece ();
		};
		var getclassforpiece = function (p, style) {
			var kind = p.kind;
			if (p.color == WHITE) {
				var kind = 'w' + kind;
			}
			return (style + 'piece') + kind;
		};
		var Square = __class__ ('Square', [object], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, file, rank) {
				self.file = file;
				self.rank = rank;
			});},
			get p () {return __get__ (this, function (self, sq) {
				return Square (self.file + sq.file, self.rank + sq.rank);
			});},
			get __repr__ () {return __get__ (this, function (self) {
				return 'Square[file: {} , rank: {}]'.format (self.file, self.rank);
			});},
			get copy () {return __get__ (this, function (self) {
				return Square (self.file, self.rank);
			});}
		});
		var Move = __class__ ('Move', [object], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, fromsq, tosq, prompiece) {
				if (typeof prompiece == 'undefined' || (prompiece != null && prompiece .hasOwnProperty ("__kwargtrans__"))) {;
					var prompiece = Piece ();
				};
				self.fromsq = fromsq;
				self.tosq = tosq;
				self.prompiece = prompiece;
			});},
			get __repr__ () {return __get__ (this, function (self) {
				return 'Move [from: {} , to: {} , prom: {}]'.format (self.fromsq, self.tosq, self.prompiece);
			});}
		});
		var PieceStore = __class__ ('PieceStore', [e], {
			__module__: __name__,
			get dragstartfactory () {return __get__ (this, function (self, p, pdiv, pdivcopy) {
				var dragstart = function (ev) {
					if (self.show) {
						ev.preventDefault ();
						return ;
					}
					self.parent.dragkind = 'set';
					self.parent.draggedsetpiece = p;
					self.parent.draggedpdiv = pdivcopy;
					self.parent.movecanvashook.x ();
					pdiv.op (0.7);
				};
				return dragstart;
			});},
			get setstore () {return __get__ (this, function (self, store) {
				self.store = store;
				self.container.x ();
				self.pieces = dict ({});
				var __iterable0__ = self.store.py_split ('');
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var pieceletter = __iterable0__ [__index0__];
					var p = piecelettertopiece (pieceletter);
					if (p.color == self.color) {
						if (__in__ (p.kind, self.pieces)) {
							self.pieces [p.kind] ['mul']++;
						}
						else {
							var pcdiv = Div ().pr ().w (self.piecesize).h (self.piecesize);
							var pdiv = Div ().pa ().cp ().ac (getclassforpiece (p, self.parent.piecestyle)).w (self.piecesize).h (self.piecesize);
							var pdivcopy = Div ().pa ().cp ().ac (getclassforpiece (p, self.parent.piecestyle)).w (self.piecesize).h (self.piecesize);
							pdiv.t (0).l (0).sa ('draggable', true).ae ('dragstart', self.dragstartfactory (p, pdiv, pdivcopy));
							pcdiv.a (pdiv);
							self.pieces [p.kind] = dict ({'mul': 1, 'p': p, 'pcdiv': pcdiv});
						}
					}
				}
				var __iterable0__ = self.pieces.py_items ();
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var __left0__ = __iterable0__ [__index0__];
					var pkind = __left0__ [0];
					var pdesc = __left0__ [1];
					var muldiv = Div ().pa ().w (self.muldivsize).h (self.muldivsize).fs (self.muldivsize * 1.3).html ('{}'.format (pdesc ['mul']));
					muldiv.l (self.piecesize - self.muldivsize).t (0).ac ('storemuldiv');
					pdesc ['pcdiv'].a (muldiv);
					self.container.a (pdesc ['pcdiv']);
				}
				return self;
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (PieceStore, '__init__') (self, 'div');
				self.show = args.py_get ('show', false);
				self.parent = args.py_get ('parent', BasicBoard (dict ({})));
				self.store = args.py_get ('store', '');
				self.color = args.py_get ('color', WHITE);
				self.container = args.py_get ('containerdiv', Div ());
				self.container.ac ('noselect');
				self.piecesize = args.py_get ('piecesize', self.parent.piecesize);
				self.muldivsize = int (self.piecesize / 2);
				self.a (self.container);
				self.setstore (self.store);
			});}
		});
		var BasicBoard = __class__ ('BasicBoard', [e], {
			__module__: __name__,
			get clearcanvases () {return __get__ (this, function (self) {
				self.movecanvas.py_clear ();
				self.piececanvashook.x ();
			});},
			get ucitosquare () {return __get__ (this, function (self, squci) {
				try {
					var file = squci.charCodeAt (0) - 'a'.charCodeAt (0);
					var rank = self.lastrank - (squci.charCodeAt (1) - '1'.charCodeAt (0));
					return Square (file, rank);
				}
				catch (__except0__) {
					return null;
				}
			});},
			get ucitomove () {return __get__ (this, function (self, moveuci) {
				if (__in__ ('@', moveuci)) {
					try {
						var parts = moveuci.py_split ('@');
						var sq = self.ucitosquare (parts [1]);
						var move = Move (sq, sq, Piece (parts [0].toLowerCase (), self.turn ()));
						return move;
					}
					catch (__except0__) {
						return null;
					}
				}
				else {
					try {
						var move = Move (self.ucitosquare (moveuci.__getslice__ (0, 2, 1)), self.ucitosquare (moveuci.__getslice__ (2, 4, 1)));
						try {
							if (len (moveuci) > 4) {
								move.prompiece = Piece (moveuci [4].toLowerCase (), self.turn ());
							}
						}
						catch (__except0__) {
							print ('could not parse prompiece');
						}
						return move;
					}
					catch (__except0__) {
						return null;
					}
				}
			});},
			get resize () {return __get__ (this, function (self, width, height) {
				self.squaresize = 35;
				self.calcsizes ();
				while (self.totalheight () < height) {
					self.squaresize++;
					self.calcsizes ();
				}
				self.squaresize--;
				self.calcsizes ();
				self.build ();
			});},
			get totalheight () {return __get__ (this, function (self) {
				var th = self.outerheight + cpick (self.showfen, self.fendivheight, 0);
				if (self.variantkey == 'crazyhouse') {
					th += 2 * self.squaresize;
				}
				return th;
			});},
			get squareuci () {return __get__ (this, function (self, sq) {
				var fileletter = String.fromCharCode (sq.file + 'a'.charCodeAt (0));
				var rankletter = String.fromCharCode ((self.lastrank - sq.rank) + '1'.charCodeAt (0));
				return fileletter + rankletter;
			});},
			get moveuci () {return __get__ (this, function (self, move) {
				var fromuci = self.squareuci (move.fromsq);
				var touci = self.squareuci (move.tosq);
				var promuci = cpick (move.prompiece.isempty (), '', move.prompiece.kind);
				return (fromuci + touci) + promuci;
			});},
			get islightfilerank () {return __get__ (this, function (self, file, rank) {
				return __mod__ (file + rank, 2) == 0;
			});},
			get islightsquare () {return __get__ (this, function (self, sq) {
				return self.islightfilerank (sq.file, sq.rank);
			});},
			get squarelist () {return __get__ (this, function (self) {
				var squarelist = list ([]);
				for (var file = 0; file < self.numfiles; file++) {
					for (var rank = 0; rank < self.numranks; rank++) {
						squarelist.append (Square (file, rank));
					}
				}
				return squarelist;
			});},
			get squarecoordsvect () {return __get__ (this, function (self, sq) {
				return Vect (sq.file * self.squaresize, sq.rank * self.squaresize);
			});},
			get squarecoordsmiddlevect () {return __get__ (this, function (self, sq) {
				return self.squarecoordsvect (sq).p (Vect (self.squaresize / 2, self.squaresize / 2));
			});},
			get piececoordsvect () {return __get__ (this, function (self, sq) {
				return self.squarecoordsvect (sq).p (Vect (self.squarepadding, self.squarepadding));
			});},
			get flipawaresquare () {return __get__ (this, function (self, sq) {
				if (self.flip) {
					return Square (self.lastfile - sq.file, self.lastrank - sq.rank);
				}
				return sq;
			});},
			get piecedragstartfactory () {return __get__ (this, function (self, sq, pdiv) {
				var piecedragstart = function (ev) {
					if (self.promoting || self.show) {
						ev.preventDefault ();
						return ;
					}
					self.dragkind = 'move';
					self.draggedsq = sq;
					self.draggedpdiv = pdiv;
					self.movecanvashook.x ();
					pdiv.op (0.1);
				};
				return piecedragstart;
			});},
			get piecedragfactory () {return __get__ (this, function (self) {
				var piecedrag = function (ev) {
					// pass;
				};
				return piecedrag;
			});},
			get piecedragendfactory () {return __get__ (this, function (self, sq, pdiv) {
				var piecedragend = function (ev) {
					pdiv.op (0.5);
				};
				return piecedragend;
			});},
			get piecedragoverfactory () {return __get__ (this, function (self, sq) {
				var piecedragover = function (ev) {
					ev.preventDefault ();
				};
				return piecedragover;
			});},
			get ismovepromotion () {return __get__ (this, function (self, move) {
				var fromp = self.getpieceatsquare (move.fromsq);
				if (fromp.kind == 'p' && fromp.color == self.turn ()) {
					if (self.iswhitesturn ()) {
						if (move.tosq.rank == 0) {
							return true;
						}
					}
					else if (move.tosq.rank == self.lastrank) {
						return true;
					}
				}
				return false;
			});},
			get piecedropfactory () {return __get__ (this, function (self, sq) {
				var piecedrop = function (ev) {
					ev.preventDefault ();
					self.draggedpdiv.pv (self.piececoordsvect (self.flipawaresquare (sq)));
					self.draggedpdiv.zi (100);
					if (self.dragkind == 'move') {
						self.dragmove = Move (self.draggedsq, sq);
						if (self.ismovepromotion (self.dragmove)) {
							self.promoting = true;
							self.build ();
						}
						else if (!(self.movecallback === null)) {
							self.movecallback (self.variantkey, self.fen, self.moveuci (self.dragmove));
						}
					}
					else if (self.dragkind == 'set') {
						self.container.a (self.draggedpdiv);
						if (!(self.movecallback === null)) {
							var setuci = '{}@{}'.format (self.draggedsetpiece.kind, self.squareuci (sq));
							self.movecallback (self.variantkey, self.fen, setuci);
						}
					}
				};
				return piecedrop;
			});},
			get buildsquares () {return __get__ (this, function (self) {
				self.container.x ();
				var __iterable0__ = self.squarelist ();
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var sq = __iterable0__ [__index0__];
					var sqclass = choose (self.islightsquare (sq), 'boardsquarelight', 'boardsquaredark');
					var sqdiv = Div ().aac (list (['boardsquare', sqclass])).w (self.squaresize).h (self.squaresize);
					var fasq = self.flipawaresquare (sq);
					sqdiv.pv (self.squarecoordsvect (fasq));
					sqdiv.ae ('dragover', self.piecedragoverfactory (sq));
					sqdiv.ae ('drop', self.piecedropfactory (sq));
					self.container.a (sqdiv);
					var p = self.getpieceatsquare (sq);
					if (p.ispiece ()) {
						var pdiv = Div ().ac ('boardpiece').w (self.piecesize).h (self.piecesize).pv (self.piececoordsvect (fasq));
						pdiv.ac (getclassforpiece (p, self.piecestyle)).sa ('draggable', true);
						pdiv.ae ('dragstart', self.piecedragstartfactory (sq, pdiv));
						pdiv.ae ('drag', self.piecedragfactory ());
						pdiv.ae ('dragend', self.piecedragendfactory (sq, pdiv));
						pdiv.ae ('dragover', self.piecedragoverfactory (sq));
						pdiv.ae ('drop', self.piecedropfactory (sq));
						pdiv.zi (10);
						if (self.variantkey == 'threeCheck') {
							if (p.kind == 'k') {
								var mul = self.getthreelifesforcolor (p.color);
								var lifesdiv = Div ().pa ().t (-(self.squaresize) / 10).l (self.squaresize / 2 + self.squaresize / 10).w (self.squaresize / 2).h (self.squaresize / 2);
								lifesdiv.ac ('boardthreechecklifesdiv').fs (self.squaresize / 1.5).html ('{}'.format (mul));
								lifesdiv.cc (p.color == WHITE, '#ff0', '#ff0');
								pdiv.a (lifesdiv);
							}
						}
						self.container.a (pdiv);
					}
				}
			});},
			get getthreelifesforcolor () {return __get__ (this, function (self, color) {
				var parts = self.threefen.py_split ('+');
				var mul = 3;
				if (color == WHITE) {
					try {
						var mul = int (parts [2]);
					}
					catch (__except0__) {
						print ('warning, could not parse white lifes from', self.threefen);
					}
				}
				if (color == BLACK) {
					try {
						var mul = int (parts [0]);
					}
					catch (__except0__) {
						print ('warning, could not parse black lifes from', self.threefen);
					}
				}
				return mul;
			});},
			get prompiececlickedfactory () {return __get__ (this, function (self, prompiecekind) {
				var prompiececlicked = function () {
					self.dragmove.prompiece = Piece (prompiecekind, self.turn ());
					self.movecallback (self.variantkey, self.fen, self.moveuci (self.dragmove));
				};
				return prompiececlicked;
			});},
			get buildprominput () {return __get__ (this, function (self) {
				var promkinds = prompiecekindsforvariantkey (self.variantkey);
				var promsq = self.dragmove.tosq.copy ();
				var dir = cpick (promsq.rank >= self.numranks / 2, -(1), 1);
				var ppks = prompiecekindsforvariantkey (self.variantkey);
				var __iterable0__ = ppks;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var ppk = __iterable0__ [__index0__];
					var fapromsq = self.flipawaresquare (promsq);
					var pp = Piece (ppk, self.turn ());
					var psqdiv = Div ().pa ().cp ().zi (150).w (self.squaresize).h (self.squaresize).ac ('boardpromotionsquare');
					psqdiv.pv (self.squarecoordsvect (fapromsq));
					var ppdiv = Div ().pa ().cp ().zi (200).w (self.piecesize).h (self.piecesize).ac (getclassforpiece (pp, self.piecestyle));
					ppdiv.pv (self.piececoordsvect (fapromsq)).ae ('mousedown', self.prompiececlickedfactory (ppk));
					self.container.aa (list ([psqdiv, ppdiv]));
					var promsq = promsq.p (Square (0, dir));
				}
			});},
			get promotecancelclick () {return __get__ (this, function (self) {
				self.promoting = false;
				self.build ();
			});},
			get drawmovearrow () {return __get__ (this, function (self, move, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				if (move === null) {
					return ;
				}
				var strokecolor = args.py_get ('strokecolor', '#FFFF00');
				var linewidth = args.py_get ('linewidth', 0.2) * self.squaresize;
				var headwidth = args.py_get ('headwidth', 0.2) * self.squaresize;
				var headheight = args.py_get ('headheight', 0.2) * self.squaresize;
				self.movecanvas.lineWidth (linewidth);
				self.movecanvas.strokeStyle (strokecolor);
				self.movecanvas.fillStyle (strokecolor);
				var tomv = self.squarecoordsmiddlevect (self.flipawaresquare (move.tosq));
				self.movecanvas.drawline (self.squarecoordsmiddlevect (self.flipawaresquare (move.fromsq)), tomv);
				var dv = Vect (headwidth, headheight);
				self.movecanvas.fillRect (tomv.m (dv), tomv.p (dv));
				if (!(move.prompiece.isempty ())) {
					var pf = 4;
					var dvp = Vect (linewidth * pf, linewidth * pf);
					move.prompiece.color = self.turn ();
					var ppdiv = Div ().pa ().cp ().ac (getclassforpiece (move.prompiece, self.piecestyle)).w ((linewidth * 2) * pf).h ((linewidth * 2) * pf);
					ppdiv.pv (tomv.m (dvp));
					self.piececanvashook.a (ppdiv);
				}
			});},
			get drawuciarrow () {return __get__ (this, function (self, uci, args) {
				if (typeof args == 'undefined' || (args != null && args .hasOwnProperty ("__kwargtrans__"))) {;
					var args = dict ({});
				};
				self.drawmovearrow (self.ucitomove (uci), args);
			});},
			get buildgenmove () {return __get__ (this, function (self) {
				if (__in__ ('genmove', self.positioninfo)) {
					if (!(genmove == 'reset')) {
						var genmoveuci = self.positioninfo ['genmove'] ['uci'];
						var genmove = self.ucitomove (genmoveuci);
						if (!(genmove === null)) {
							genmove.prompiece = Piece ();
							self.drawmovearrow (genmove);
						}
					}
				}
			});},
			get build () {return __get__ (this, function (self) {
				self.sectioncontainer = Div ().ac ('boardsectioncontainer').w (self.outerwidth);
				self.outercontainer = Div ().ac ('boardoutercontainer').w (self.outerwidth).h (self.outerheight);
				self.container = Div ().ac ('boardcontainer').w (self.width).h (self.height).t (self.margin).l (self.margin);
				self.outercontainer.a (self.container);
				self.buildsquares ();
				self.turndiv = Div ().pa ().w (self.turndivsize).h (self.turndivsize).cbc (self.iswhitesturn (), '#fff', '#000');
				if (self.variantkey == 'racingKings') {
					self.turndiv.ct (self.flip, 0, self.outerheight - self.turndivsize).cl (xor (self.isblacksturn (), self.flip), 0, self.outerwidth - self.turndivsize);
				}
				else {
					self.turndiv.l (self.outerwidth - self.turndivsize).ct (xor (self.isblacksturn (), self.flip), 0, self.outerheight - self.turndivsize);
				}
				self.outercontainer.a (self.turndiv);
				if (self.promoting) {
					self.buildprominput ();
					self.container.ae ('mousedown', self.promotecancelclick);
				}
				self.fentext = RawTextInput (dict ({})).w (self.width).fs (10).setText (self.fen);
				self.fendiv = Div ().ac ('boardfendiv').h (self.fendivheight).a (self.fentext);
				if (self.variantkey == 'crazyhouse') {
					self.whitestorediv = Div ().ac ('boardstorediv').h (self.squaresize).w (self.outerwidth);
					self.blackstorediv = Div ().ac ('boardstorediv').h (self.squaresize).w (self.outerwidth);
					self.whitestore = PieceStore (dict ({'show': self.show, 'parent': self, 'color': WHITE, 'store': self.crazyfen, 'containerdiv': self.whitestorediv}));
					self.blackstore = PieceStore (dict ({'show': self.show, 'parent': self, 'color': BLACK, 'store': self.crazyfen, 'containerdiv': self.blackstorediv}));
					if (self.flip) {
						self.sectioncontainer.aa (list ([self.whitestorediv, self.outercontainer, self.blackstorediv]));
					}
					else {
						self.sectioncontainer.aa (list ([self.blackstorediv, self.outercontainer, self.whitestorediv]));
					}
				}
				else {
					self.sectioncontainer.aa (list ([self.outercontainer]));
				}
				if (self.showfen) {
					self.sectioncontainer.a (self.fendiv);
				}
				self.x ().a (self.sectioncontainer);
				self.movecanvas = Canvas (self.width, self.height).pa ().t (0).l (0);
				self.movecanvashook = Div ().pa ().t (0).l (0).zi (5).op (0.5);
				self.piececanvashook = Div ().pa ().t (0).l (0).zi (11).op (0.5);
				self.container.aa (list ([self.movecanvashook, self.piececanvashook]));
				self.movecanvashook.a (self.movecanvas);
				self.buildgenmove ();
				return self;
			});},
			get setflip () {return __get__ (this, function (self, flip) {
				self.flip = flip;
				self.build ();
			});},
			get calcsizes () {return __get__ (this, function (self) {
				self.lastfile = self.numfiles - 1;
				self.lastrank = self.numranks - 1;
				self.area = self.numfiles * self.numranks;
				self.width = self.numfiles * self.squaresize;
				self.height = self.numranks * self.squaresize;
				self.avgsize = (self.width + self.height) / 2;
				self.margin = self.marginratio * self.avgsize;
				self.squarepadding = self.squarepaddingratio * self.squaresize;
				self.piecesize = self.squaresize - 2 * self.squarepadding;
				self.outerwidth = self.width + 2 * self.margin;
				self.outerheight = self.height + 2 * self.margin;
				self.turndivsize = self.margin;
				self.fendivheight = 25;
			});},
			get parseargs () {return __get__ (this, function (self, args) {
				self.positioninfo = args.py_get ('positioninfo', dict ({}));
				self.show = args.py_get ('show', false);
				self.showfen = args.py_get ('showfen', true);
				self.squaresize = args.py_get ('squaresize', 45);
				self.squarepaddingratio = args.py_get ('squarepaddingratio', 0.04);
				self.marginratio = args.py_get ('marginratio', 0.02);
				self.numfiles = args.py_get ('numfiles', 8);
				self.numranks = args.py_get ('numranks', 8);
				self.piecestyle = args.py_get ('piecestyle', 'alpha');
				self.flip = args.py_get ('flip', false);
				self.movecallback = args.py_get ('movecallback', null);
				self.calcsizes ();
			});},
			get setpieceati () {return __get__ (this, function (self, i, p) {
				if (i >= 0 && i < self.area) {
					self.rep [i] = p;
				}
				else {
					print ('warning, rep index out of range', i);
				}
			});},
			get getpieceati () {return __get__ (this, function (self, i) {
				if (i >= 0 && i < self.area) {
					return self.rep [i];
				}
				return Piece ();
			});},
			get getpieceatfilerank () {return __get__ (this, function (self, file, rank) {
				var i = rank * self.numfiles + file;
				return self.getpieceati (i);
			});},
			get getpieceatsquare () {return __get__ (this, function (self, sq) {
				return self.getpieceatfilerank (sq.file, sq.rank);
			});},
			get setrepfromfen () {return __get__ (this, function (self, fen) {
				self.fen = fen;
				self.crazyfen = null;
				self.threefen = null;
				self.rep = (function () {
					var __accu0__ = [];
					for (var i = 0; i < self.area; i++) {
						__accu0__.append (Piece ());
					}
					return __accu0__;
				}) ();
				var fenparts = self.fen.py_split (' ');
				self.rawfen = fenparts [0];
				var rawfenparts = self.rawfen.py_split ('/');
				if (self.variantkey == 'crazyhouse') {
					self.crazyfen = '';
					if (__in__ ('[', self.rawfen)) {
						var cfenparts = self.rawfen.py_split ('[');
						self.rawfen = cfenparts [0];
						var rawfenparts = self.rawfen.py_split ('/');
						var cfenparts = cfenparts [1].py_split (']');
						self.crazyfen = cfenparts [0];
					}
				}
				var i = 0;
				var __iterable0__ = rawfenparts;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var rawfenpart = __iterable0__ [__index0__];
					var pieceletters = rawfenpart.py_split ('');
					var __iterable1__ = pieceletters;
					for (var __index1__ = 0; __index1__ < len (__iterable1__); __index1__++) {
						var pieceletter = __iterable1__ [__index1__];
						if (isvalidpieceletter (pieceletter)) {
							self.setpieceati (i, piecelettertopiece (pieceletter));
							i++;
						}
						else {
							var mul = 0;
							try {
								var mul = int (pieceletter);
							}
							catch (__except0__) {
								print ('warning, multiplicity could not be parsed from', pieceletter);
							}
							for (var j = 0; j < mul; j++) {
								self.setpieceati (i, Piece ());
								i++;
							}
						}
					}
				}
				if (i < self.area) {
					print ('warning, raw fen did not fill board');
				}
				else if (i > self.area) {
					print ('warning, raw fen exceeded board');
				}
				self.turnfen = 'w';
				if (len (fenparts) > 1) {
					self.turnfen = fenparts [1];
				}
				else {
					print ('warning, no turn fen');
				}
				self.castlefen = '-';
				if (len (fenparts) > 2) {
					self.castlefen = fenparts [2];
				}
				else {
					print ('warning, no castle fen');
				}
				self.epfen = '-';
				if (len (fenparts) > 3) {
					self.epfen = fenparts [3];
				}
				else {
					print ('warning, no ep fen');
				}
				var moveclocksi = cpick (self.variantkey == 'threeCheck', 5, 4);
				self.halfmoveclock = 0;
				if (len (fenparts) > moveclocksi) {
					try {
						self.halfmoveclock = int (fenparts [moveclocksi]);
					}
					catch (__except0__) {
						print ('warning, half move clock could not be parsed from', fenparts [4]);
					}
				}
				else {
					print ('warning, no half move fen');
				}
				self.fullmovenumber = 1;
				if (len (fenparts) > moveclocksi + 1) {
					try {
						self.fullmovenumber = int (fenparts [moveclocksi + 1]);
					}
					catch (__except0__) {
						print ('warning, full move number could not be parsed from', fenparts [5]);
					}
				}
				else {
					print ('warning, no full move fen');
				}
				if (self.variantkey == 'threeCheck') {
					if (len (fenparts) > 4) {
						self.threefen = fenparts [4];
					}
				}
				self.promoting = false;
			});},
			get turn () {return __get__ (this, function (self) {
				if (self.turnfen == 'w') {
					return WHITE;
				}
				return BLACK;
			});},
			get iswhitesturn () {return __get__ (this, function (self) {
				return self.turn () == WHITE;
			});},
			get isblacksturn () {return __get__ (this, function (self) {
				return self.turn () == BLACK;
			});},
			get initrep () {return __get__ (this, function (self, args) {
				self.variantkey = args.py_get ('variantkey', 'standard');
				self.setrepfromfen (args.py_get ('fen', getstartfenforvariantkey (self.variantkey)));
			});},
			get setfromfen () {return __get__ (this, function (self, fen, positioninfo) {
				if (typeof positioninfo == 'undefined' || (positioninfo != null && positioninfo .hasOwnProperty ("__kwargtrans__"))) {;
					var positioninfo = dict ({});
				};
				self.positioninfo = positioninfo;
				self.setrepfromfen (fen);
				self.build ();
			});},
			get reset () {return __get__ (this, function (self) {
				self.setfromfen (getstartfenforvariantkey (self.variantkey));
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (BasicBoard, '__init__') (self, 'div');
				self.positioninfo = dict ({});
				self.parseargs (args);
				self.initrep (args);
				self.build ();
			});}
		});
		var MultipvInfo = __class__ ('MultipvInfo', [e], {
			__module__: __name__,
			get bestmovesanclickedfactory () {return __get__ (this, function (self, moveuci) {
				var bestmovesanclicked = function () {
					if (!(self.bestmovesanclickedcallback === null)) {
						self.bestmovesanclickedcallback (moveuci);
					}
				};
				return bestmovesanclicked;
			});},
			get scorebonus () {return __get__ (this, function (self) {
				if (__in__ ('scorebonus', self.infoi)) {
					try {
						var scorebonus = int (self.infoi ['scorebonus']);
						return scorebonus;
					}
					catch (__except0__) {
						// pass;
					}
				}
				return 0;
			});},
			get effscore () {return __get__ (this, function (self) {
				return self.scorenumerical + self.scorebonus ();
			});},
			get bonussliderchanged () {return __get__ (this, function (self) {
				self.infoi ['scorebonus'] = self.bonusslider.v ();
				self.build ();
				if (!(self.bonussliderchangedcallback === null)) {
					self.bonussliderchangedcallback ();
				}
			});},
			get build () {return __get__ (this, function (self) {
				self.bestmoveuci = self.infoi ['bestmoveuci'];
				self.bestmovesan = self.infoi ['bestmovesan'];
				self.scorenumerical = self.infoi ['scorenumerical'];
				self.pvsan = self.infoi ['pvsan'];
				self.pvpgn = self.infoi ['pvpgn'];
				self.depth = self.infoi ['depth'];
				self.nps = self.infoi ['nps'];
				self.container = Div ().ac ('multipvinfocontainer');
				self.idiv = Div ().ac ('multipvinfoi').html ('{}.'.format (self.i));
				self.bestmovesandiv = Div ().ac ('multipvinfobestmovesan').html (self.bestmovesan);
				self.bestmovesandiv.ae ('mousedown', self.bestmovesanclickedfactory (self.bestmoveuci));
				self.scorenumericaldiv = Div ().ac ('multipvinfoscorenumerical').html ('{}'.format (scoreverbal (self.effscore ())));
				self.bonussliderdiv = Div ().ac ('multipvinfobonussliderdiv');
				self.bonusslider = Slider ().setmin (-(500)).setmax (500).ac ('multipvinfobonusslider').sv (self.scorebonus ());
				self.bonusslider.ae ('change', self.bonussliderchanged);
				self.bonussliderdiv.a (self.bonusslider);
				self.depthdiv = Div ().ac ('multipvinfodepth').html ('{}'.format (self.depth));
				self.miscdiv = Div ().ac ('multipvinfomisc').html ('nps {}'.format (self.nps));
				self.pvdiv = Div ().ac ('multipvinfopv').html (self.pvpgn);
				self.container.aa (list ([self.idiv, self.bestmovesandiv, self.scorenumericaldiv, self.bonussliderdiv, self.depthdiv, self.miscdiv, self.pvdiv]));
				self.bestmovesandiv.c (scorecolor (self.effscore ()));
				self.scorenumericaldiv.c (scorecolor (self.effscore ()));
				self.x ().a (self.container);
			});},
			get __init__ () {return __get__ (this, function (self, infoi) {
				__super__ (MultipvInfo, '__init__') (self, 'div');
				self.bestmovesanclickedcallback = null;
				self.bonussliderchangedcallback = null;
				self.infoi = infoi;
				self.i = self.infoi ['i'];
				self.build ();
			});}
		});
		var PgnInfo = __class__ ('PgnInfo', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, parent) {
				__super__ (PgnInfo, '__init__') (self, 'div');
				self.headers = list ([]);
				self.parent = parent;
			});},
			get getheader () {return __get__ (this, function (self, key, py_default) {
				var __iterable0__ = self.headers;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var header = __iterable0__ [__index0__];
					if (header [0] == key) {
						return header [1];
					}
				}
				return py_default;
			});},
			get playerlink () {return __get__ (this, function (self, username) {
				return "<a href='https://lichess.org/@/{}' target='_blank' rel='noopener noreferrer'>{}</a>".format (username, username);
			});},
			get parsecontent () {return __get__ (this, function (self) {
				var lines = self.content.py_split ('\n');
				self.headers = list ([]);
				var __iterable0__ = lines;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var line = __iterable0__ [__index0__];
					if (line [0] == '[') {
						var parts = line.__getslice__ (1, null, 1).py_split ('"');
						var key = parts [0].py_split (' ') [0];
						var value = parts [1].py_split ('"') [0];
						self.headers.append (tuple ([key, value]));
					}
				}
				self.white = self.getheader ('White', '?');
				self.black = self.getheader ('Black', '?');
				self.result = self.getheader ('Result', '?');
				self.site = self.getheader ('Site', '');
				self.whiteelo = self.getheader ('WhiteElo', '?');
				self.whiteratingdiff = self.getheader ('WhiteRatingDiff', '?');
				self.blackelo = self.getheader ('BlackElo', '?');
				self.blackratingdiff = self.getheader ('BlackRatingDiff', '?');
				self.variant = self.getheader ('Variant', 'Standard');
				self.timecontrol = self.getheader ('TimeControl', '?');
				self.id = self.site.py_split ('/').__getslice__ (-(1), null, 1) [0];
			});},
			get idclicked () {return __get__ (this, function (self) {
				self.parent.pgntext.setpgn (self.content);
				self.parent.sioreq (dict ({'kind': 'parsepgn', 'owner': 'board', 'data': self.content}));
			});},
			get mecolor () {return __get__ (this, function (self) {
				if (self.white == self.parent.username) {
					return WHITE;
				}
				if (self.black == self.parent.username) {
					return BLACK;
				}
				return null;
			});},
			get mewhite () {return __get__ (this, function (self) {
				return self.mecolor () == WHITE;
			});},
			get meblack () {return __get__ (this, function (self) {
				return self.mecolor () == BLACK;
			});},
			get hasme () {return __get__ (this, function (self) {
				return !(self.mecolor () === null);
			});},
			get score () {return __get__ (this, function (self) {
				if (self.result == '1-0') {
					return 1;
				}
				if (self.result == '0-1') {
					return 0;
				}
				return 0.5;
			});},
			get mescore () {return __get__ (this, function (self) {
				if (self.hasme ()) {
					if (self.mewhite ()) {
						return self.score ();
					}
					return 1 - self.score ();
				}
				return self.score ();
			});},
			get build () {return __get__ (this, function (self) {
				self.x ().ac ('pgninfocontainer');
				self.tcdiv = Div ().ac ('pgninfotcdiv').html ('{} {}'.format (self.timecontrol, self.variant));
				self.whitediv = Div ().ac ('pgninfoplayerdiv').html (self.playerlink (self.white));
				self.whiteelodiv = Div ().ac ('pgninfoplayerelodiv').html ('{} {}'.format (self.whiteelo, self.whiteratingdiff));
				self.whitediv.acc (self.meblack (), 'pgninfotheyplayerdiv');
				self.blackdiv = Div ().ac ('pgninfoplayerdiv').html (self.playerlink (self.black));
				self.blackelodiv = Div ().ac ('pgninfoplayerelodiv').html ('{} {}'.format (self.blackelo, self.blackratingdiff));
				self.blackdiv.acc (self.mewhite (), 'pgninfotheyplayerdiv');
				self.resultdiv = Div ().ac ('pgninforesultdiv').html (self.result);
				self.iddiv = Div ().ac ('pgninfoiddiv').html (self.id);
				self.iddiv.ae ('mousedown', self.idclicked);
				var mescore = self.mescore ();
				if (mescore == 1) {
					self.ac ('pgninfowhitewin');
				}
				else if (mescore == 0) {
					self.ac ('pgninfoblackwin');
				}
				else {
					self.ac ('pgninfodraw');
				}
				self.aa (list ([self.tcdiv, self.whitediv, self.whiteelodiv, self.blackdiv, self.blackelodiv, self.resultdiv, self.iddiv]));
				return self;
			});},
			get setcontent () {return __get__ (this, function (self, content) {
				self.content = content;
				self.parsecontent ();
				return self.build ();
			});}
		});
		var PgnList = __class__ ('PgnList', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self, parent) {
				__super__ (PgnList, '__init__') (self, 'div');
				self.parent = parent;
			});},
			get build () {return __get__ (this, function (self) {
				self.x ();
				var __iterable0__ = self.gamecontents;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var gamecontent = __iterable0__ [__index0__];
					self.a (PgnInfo (self.parent).setcontent (gamecontent));
				}
				return self;
			});},
			get setcontent () {return __get__ (this, function (self, content) {
				self.content = content;
				self.gamecontents = self.content.py_split ('\n\n\n').__getslice__ (0, -(1), 1);
				return self.build ();
			});}
		});
		var PgnText = __class__ ('PgnText', [e], {
			__module__: __name__,
			get __init__ () {return __get__ (this, function (self) {
				__super__ (PgnText, '__init__') (self, 'div');
				self.ac ('pgntextcontainer');
				self.textarea = TextArea ();
				self.a (self.textarea);
				self.resize (600, 300);
			});},
			get setpgn () {return __get__ (this, function (self, pgn) {
				self.textarea.setText (pgn);
				return self;
			});},
			get getpgn () {return __get__ (this, function (self) {
				return self.textarea.getText ();
			});},
			get resize () {return __get__ (this, function (self, width, height) {
				self.width = width;
				self.height = height;
				self.textarea.w (width - 15).h (height - 15);
				return self;
			});}
		});
		var Board = __class__ ('Board', [e], {
			__module__: __name__,
			get flipcallback () {return __get__ (this, function (self) {
				self.basicboard.setflip (!(self.basicboard.flip));
			});},
			get resetcallback () {return __get__ (this, function (self) {
				self.basicboard.reset ();
			});},
			get setfromfen () {return __get__ (this, function (self, fen, positioninfo, edithistory) {
				if (typeof positioninfo == 'undefined' || (positioninfo != null && positioninfo .hasOwnProperty ("__kwargtrans__"))) {;
					var positioninfo = dict ({});
				};
				if (typeof edithistory == 'undefined' || (edithistory != null && edithistory .hasOwnProperty ("__kwargtrans__"))) {;
					var edithistory = true;
				};
				var restartanalysis = false;
				if (self.analyzing.py_get ()) {
					self.stopanalyzecallback ();
					var restartanalysis = true;
				}
				if (edithistory && __in__ ('genmove', positioninfo)) {
					var genmove = positioninfo ['genmove'];
					if (genmove == 'reset') {
						self.history = list ([]);
					}
					else {
						self.history.append (dict ({'fen': self.basicboard.fen, 'positioninfo': self.positioninfo}));
					}
				}
				self.positioninfo = positioninfo;
				self.movelist = cpick (__in__ ('movelist', self.positioninfo), self.positioninfo ['movelist'], list ([]));
				self.basicboard.setfromfen (fen, self.positioninfo);
				self.buildpositioninfo ();
				self.analysisinfodiv.x ();
				if (restartanalysis) {
					self.analyzecallbackfactory () ();
				}
				self.getstoredanalysisinfo ();
			});},
			get getstoredanalysisinfo () {return __get__ (this, function (self) {
				if (!(self.analyzing.py_get ())) {
					self.sioreq (dict ({'kind': 'retrievedb', 'owner': 'board', 'path': 'analysisinfo/{}/{}'.format (self.basicboard.variantkey, self.positioninfo ['zobristkeyhex'])}));
				}
			});},
			get setvariantcombo () {return __get__ (this, function (self) {
				self.variantcombo.setoptions (VARIANT_OPTIONS, self.basicboard.variantkey);
			});},
			get sioreq () {return __get__ (this, function (self, obj) {
				if (!(self.socket === null)) {
					self.socket.emit ('sioreq', obj);
				}
			});},
			get posclickedfactory () {return __get__ (this, function (self, i) {
				var poslicked = function () {
					self.gamei = i;
					var pinfo = self.positioninfos [i];
					self.setfromfen (pinfo ['fen'], pinfo ['positioninfo']);
					for (var j = 0; j < len (self.positioninfos); j++) {
						self.posdivs [j].arc (j == self.gamei, 'boardposdivselected');
					}
					self.history = list ([]);
				};
				return poslicked;
			});},
			get selectgamei () {return __get__ (this, function (self, i) {
				if (len (self.positioninfos) > 0) {
					self.posclickedfactory (i) ();
				}
			});},
			get gamehere () {return __get__ (this, function (self) {
				self.selectgamei (self.gamei);
			});},
			get gametobegin () {return __get__ (this, function (self) {
				self.gamei = 0;
				self.selectgamei (self.gamei);
			});},
			get gameback () {return __get__ (this, function (self) {
				self.gamei--;
				if (self.gamei < 0) {
					self.gamei = 0;
				}
				self.selectgamei (self.gamei);
			});},
			get gameforward () {return __get__ (this, function (self) {
				self.gamei++;
				if (self.gamei >= len (self.positioninfos)) {
					self.gamei = len (self.positioninfos) - 1;
				}
				self.selectgamei (self.gamei);
			});},
			get gametoend () {return __get__ (this, function (self) {
				self.gamei = len (self.positioninfos) - 1;
				self.selectgamei (self.gamei);
			});},
			get buildgame () {return __get__ (this, function (self) {
				self.gamediv.x ();
				self.posdivs = list ([]);
				var i = 0;
				var __iterable0__ = self.positioninfos;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var pinfo = __iterable0__ [__index0__];
					var fen = pinfo ['fen'];
					var posinfo = pinfo ['positioninfo'];
					var genmove = '*';
					if (__in__ ('genmove', posinfo)) {
						var genmove = posinfo ['genmove'] ['san'];
					}
					var posdiv = Div ().ac ('boardposdiv');
					self.posdivs.append (posdiv);
					posdiv.ae ('mousedown', self.posclickedfactory (i));
					var movediv = Div ().ac ('boardposmovediv').html (genmove);
					var fendiv = Div ().ac ('boardposfendiv');
					var showboard = BasicBoard (dict ({'show': true, 'showfen': false, 'positioninfo': posinfo, 'fen': fen, 'squaresize': 20, 'flip': self.flip}));
					fendiv.a (showboard);
					posdiv.aa (list ([movediv, fendiv]));
					self.gamediv.a (posdiv);
					i++;
				}
				self.gamei = 0;
				self.gamehere ();
			});},
			get siores () {return __get__ (this, function (self, response) {
				try {
					if (__in__ ('dataobj', response)) {
						var dataobj = response ['dataobj'];
						if (__in__ ('variantkey', dataobj)) {
							self.variantchanged (dataobj ['variantkey']);
						}
						else if (__in__ ('analysisinfo', dataobj)) {
							self.processanalysisinfo (dataobj ['analysisinfo'], true);
						}
					}
					if (__in__ ('historyobj', response)) {
						var historyobj = response ['historyobj'];
						var uci_variant = historyobj ['uci_variant'];
						var chess960 = historyobj ['chess960'];
						var pgn = historyobj ['pgn'];
						var pgninfo = PgnInfo (self).setcontent (pgn);
						var vk = uci_variant_to_variantkey (uci_variant, chess960);
						self.variantchanged (vk, false);
						self.flip = pgninfo.meblack ();
						self.basicboard.setflip (self.flip);
						self.positioninfos = historyobj ['positioninfos'];
						self.buildgame ();
						self.tabpane.selectByKey ('analysis');
					}
				}
				catch (__except0__) {
					print ('error processing siores', response);
				}
			});},
			get variantchanged () {return __get__ (this, function (self, variantkey, docallback) {
				if (typeof docallback == 'undefined' || (docallback != null && docallback .hasOwnProperty ("__kwargtrans__"))) {;
					var docallback = true;
				};
				self.basicboard.variantkey = variantkey;
				self.basicboard.reset ();
				try {
					self.basicboard.resize (self.resizewidth, self.resizeheight);
				}
				catch (__except0__) {
					// pass;
				}
				try {
					self.resizetabpanewidth (self.resizewidth);
				}
				catch (__except0__) {
					// pass;
				}
				if (!(self.variantchangedcallback === null) && docallback) {
					self.variantchangedcallback (self.basicboard.variantkey);
				}
				self.basicresize ();
				self.buildpositioninfo ();
				self.setvariantcombo ();
				self.sioreq (dict ({'kind': 'storedb', 'path': 'board/variantkey', 'dataobj': dict ({'variantkey': self.basicboard.variantkey})}));
			});},
			get setvariantcallback () {return __get__ (this, function (self) {
				self.variantchanged (self.basicboard.variantkey);
			});},
			get moveclickedfactory () {return __get__ (this, function (self, move) {
				var moveclicked = function () {
					if (!(self.moveclickedcallback === null)) {
						self.moveclickedcallback (self.basicboard.variantkey, self.basicboard.fen, move ['uci']);
					}
				};
				return moveclicked;
			});},
			get buildpositioninfo () {return __get__ (this, function (self) {
				self.movelistdiv.x ().h (self.totalheight ());
				var __iterable0__ = self.movelist;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var move = __iterable0__ [__index0__];
					var movediv = Div ().ac ('bigboardshowmove').html (move ['san']);
					movediv.ae ('mousedown', self.moveclickedfactory (move));
					self.movelistdiv.a (movediv);
				}
			});},
			get delcallback () {return __get__ (this, function (self) {
				if (len (self.history) > 0) {
					var item = self.history.py_pop ();
					self.setfromfen (item ['fen'], item ['positioninfo'], false);
				}
			});},
			get totalheight () {return __get__ (this, function (self) {
				return self.basicboard.totalheight () + self.controlpanelheight;
			});},
			get controlwidth () {return __get__ (this, function (self) {
				return max (self.basicboard.outerwidth, self.controlpanelwidth);
			});},
			get totalwidth () {return __get__ (this, function (self) {
				return self.controlwidth () + self.movelistdivwidth;
			});},
			get basicresize () {return __get__ (this, function (self) {
				self.controlpanel.w (self.controlwidth ()).mw (self.controlwidth ());
				self.sectioncontainer.w (self.controlwidth ());
				self.tabpane.resize (null, self.totalheight ());
			});},
			get resizetabpanewidth () {return __get__ (this, function (self, width) {
				self.tabpane.resize (max (width - self.totalwidth (), 600), null);
			});},
			get resizetask () {return __get__ (this, function (self) {
				self.resizewidth = self.resizeorigwidth;
				self.resizeheight = self.resizeorigheight - self.controlpanelheight;
				self.basicboard.resize (self.resizewidth, self.resizeheight);
				self.basicresize ();
				self.buildpositioninfo ();
				self.resizetabpanewidth (self.resizeorigwidth);
			});},
			get resize () {return __get__ (this, function (self, width, height) {
				self.resizeorigwidth = width;
				self.resizeorigheight = height;
				self.resizetask ();
			});},
			get analyzecallbackfactory () {return __get__ (this, function (self, all, depthlimit, timelimit) {
				if (typeof all == 'undefined' || (all != null && all .hasOwnProperty ("__kwargtrans__"))) {;
					var all = false;
				};
				if (typeof depthlimit == 'undefined' || (depthlimit != null && depthlimit .hasOwnProperty ("__kwargtrans__"))) {;
					var depthlimit = null;
				};
				if (typeof timelimit == 'undefined' || (timelimit != null && timelimit .hasOwnProperty ("__kwargtrans__"))) {;
					var timelimit = null;
				};
				var analyzecallback = function () {
					self.anyinfo = false;
					self.depthlimit = depthlimit;
					self.timelimit = timelimit;
					self.analysisstartedat = new Date ().getTime ();
					self.bestmoveuci = null;
					self.analyzing.set (true);
					if (!(self.enginecommandcallback === null)) {
						var mpv = cpick (all, 200, self.getmultipv ());
						self.enginecommandcallback ('analyze {} {} {}'.format (self.basicboard.variantkey, mpv, self.basicboard.fen));
					}
				};
				return analyzecallback;
			});},
			get stopanalyzecallback () {return __get__ (this, function (self) {
				self.analyzing.set (false);
				self.basicboard.clearcanvases ();
				if (!(self.enginecommandcallback === null)) {
					self.enginecommandcallback ('stopanalyze');
				}
			});},
			get analysismoveclicked () {return __get__ (this, function (self, moveuci) {
				if (!(self.moveclickedcallback === null)) {
					self.moveclickedcallback (self.basicboard.variantkey, self.basicboard.fen, moveuci);
				}
			});},
			get buildanalysisinfodiv () {return __get__ (this, function (self) {
				self.analysisinfodiv.x ();
				self.basicboard.clearcanvases ();
				self.maxdepth = 0;
				var minfos = list ([]);
				var __iterable0__ = self.analysisinfo ['pvitems'];
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var infoi = __iterable0__ [__index0__];
					try {
						var minfo = MultipvInfo (infoi);
						minfo.bestmovesanclickedcallback = self.analysismoveclicked;
						minfo.bonussliderchangedcallback = self.buildanalysisinfodiv;
						if (minfo.depth > self.maxdepth) {
							self.maxdepth = minfo.depth;
						}
						minfos.append (minfo);
					}
					catch (__except0__) {
						// pass;
					}
				}
				var i = 1;
				var __iterable0__ = sorted (minfos, __kwargtrans__ ({key: (function __lambda__ (item) {
					return item.effscore ();
				}), reverse: true}));
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var minfo = __iterable0__ [__index0__];
					minfo.i = i;
					minfo.build ();
					if (i == 1) {
						self.bestmoveuci = minfo.bestmoveuci;
					}
					var iw = 1 / (5 * i);
					self.basicboard.drawuciarrow (minfo.bestmoveuci, dict ({'strokecolor': scorecolor (minfo.effscore ()), 'linewidth': iw, 'headheight': iw}));
					self.analysisinfodiv.a (minfo);
					i++;
				}
			});},
			get processanalysisinfo () {return __get__ (this, function (self, obj, force) {
				if (typeof force == 'undefined' || (force != null && force .hasOwnProperty ("__kwargtrans__"))) {;
					var force = false;
				};
				if (!(self.analyzing) && !(force)) {
					return ;
				}
				self.anyinfo = true;
				var elapsed = new Date ().getTime () - self.analysisstartedat;
				self.analysisinfo = obj;
				self.buildanalysisinfodiv ();
				if (self.analyzing.py_get () && !(self.depthlimit === null) || !(self.timelimit === null)) {
					var depthok = self.depthlimit === null || self.maxdepth >= self.depthlimit;
					var timeok = self.timelimit === null || elapsed >= self.timelimit;
					if (depthok && timeok) {
						self.stopandstoreanalysis ();
					}
				}
			});},
			get stopandstoreanalysis () {return __get__ (this, function (self) {
				self.stopanalyzecallback ();
				if (!(self.anyinfo)) {
					return ;
				}
				self.storeanalysiscallback ();
			});},
			get makeanalyzedmovecallback () {return __get__ (this, function (self) {
				if (!(self.bestmoveuci === null)) {
					if (!(self.moveclickedcallback === null)) {
						self.moveclickedcallback (self.basicboard.variantkey, self.basicboard.fen, self.bestmoveuci);
					}
				}
			});},
			get storeanalysiscallback () {return __get__ (this, function (self) {
				if (!(self.analysisinfo === null)) {
					self.sioreq (dict ({'kind': 'storedb', 'path': 'analysisinfo/{}/{}'.format (self.basicboard.variantkey, self.analysisinfo ['zobristkeyhex']), 'dataobj': dict ({'analysisinfo': self.analysisinfo})}));
				}
				else {
					window.alert ('No analysis to store.');
				}
			});},
			get getmultipv () {return __get__ (this, function (self) {
				try {
					var multipv = int (self.multipvcombo.select.v ());
					return multipv;
				}
				catch (__except0__) {
					return self.defaultmultipv;
				}
			});},
			get analyzingchangedcallback () {return __get__ (this, function (self) {
				self.analysiscontrolpanelbottom.cbc (self.analyzing.py_get (), '#afa', '#edd');
			});},
			get getconfigscalar () {return __get__ (this, function (self, path, py_default) {
				if (self.configschema === null) {
					return py_default;
				}
				var found = getscalarfromschema (self.configschema, path);
				if (found === null) {
					return py_default;
				}
				return found;
			});},
			get getconfigbool () {return __get__ (this, function (self, path, py_default) {
				var s = self.getconfigscalar (path, null);
				if (s === null) {
					return py_default;
				}
				if (s == 'true') {
					return true;
				}
				if (s == 'false') {
					return false;
				}
				return py_default;
			});},
			get getconfigint () {return __get__ (this, function (self, path, py_default) {
				var s = self.getconfigscalar (path, null);
				if (s === null) {
					return py_default;
				}
				try {
					var i = int (s);
					return i;
				}
				catch (__except0__) {
					return py_default;
				}
			});},
			get gamesloadedok () {return __get__ (this, function (self, content) {
				self.pgnlist = PgnList (self).setcontent (content);
				self.gamesdiv.x ();
				self.gamesdiv.a (Button ('Reload', self.loadgames));
				self.gamesdiv.a (self.gamesloadingdiv.x ());
				self.gamesdiv.a (self.pgnlist);
			});},
			get loadgames () {return __get__ (this, function (self) {
				self.gamesloadingdiv.html ('Games loading...');
				if (!(self.username === null)) {
					lichapiget ('{}/{}?max={}'.format (LICH_API_GAMES_EXPORT, self.username, self.maxgames), self.usertoken, self.gamesloadedok, (function __lambda__ (err) {
						return print (err);
					}));
				}
			});},
			get setconfigschema () {return __get__ (this, function (self, configschema) {
				self.configschema = configschema;
				self.username = self.getconfigscalar ('global/username', null);
				self.usertoken = self.getconfigscalar ('global/usertoken', null);
				self.showfen = self.getconfigbool ('global/showfen', true);
				self.maxgames = self.getconfigint ('global/maxgames', 25);
				self.basicboard.showfen = self.showfen;
				self.resizetask ();
				self.loadgames ();
			});},
			get storeforward () {return __get__ (this, function (self) {
				self.storeanalysiscallback ();
				self.gameforward ();
			});},
			get storemake () {return __get__ (this, function (self) {
				self.storeanalysiscallback ();
				self.makeanalyzedmovecallback ();
			});},
			get __init__ () {return __get__ (this, function (self, args) {
				__super__ (Board, '__init__') (self, 'div');
				self.maxgames = 25;
				self.resizeorigwidth = 800;
				self.resizeorigheight = 400;
				self.showfen = true;
				self.flip = false;
				self.gamesloadingdiv = Div ();
				self.positioninfos = list ([]);
				self.pgnlist = null;
				self.username = null;
				self.usertoken = null;
				self.configschema = null;
				self.depthlimit = null;
				self.analysisinfo = null;
				self.defaultmultipv = 3;
				self.bestmoveuci = null;
				self.analyzing = View (self.analyzingchangedcallback, false);
				self.history = list ([]);
				self.basicboard = BasicBoard (args);
				self.controlpanel = Div ().ac ('boardcontrolpanel');
				self.controlpanelheight = getglobalcssvarpxint ('--boardcontrolpanelheight');
				self.controlpanelwidth = 260;
				self.controlpanel.a (Button ('Flip', self.flipcallback));
				self.variantcombo = ComboBox (dict ({'changecallback': self.variantchanged, 'selectclass': 'variantselect', 'optionfirstclass': 'variantoptionfirst', 'optionclass': 'variantoption'}));
				self.setvariantcombo ();
				self.variantchangedcallback = args.py_get ('variantchangedcallback', null);
				self.moveclickedcallback = args.py_get ('moveclickedcallback', null);
				self.enginecommandcallback = args.py_get ('enginecommandcallback', null);
				self.socket = args.py_get ('socket', null);
				self.controlpanel.a (self.variantcombo).w (self.basicboard.outerwidth).mw (self.basicboard.outerwidth);
				self.controlpanel.a (Button ('Del', self.delcallback));
				self.controlpanel.a (Button ('Reset', self.setvariantcallback));
				self.sectioncontainer = Div ().ac ('bigboardsectioncontainer').w (self.basicboard.outerwidth);
				self.sectioncontainer.aa (list ([self.controlpanel, self.basicboard]));
				self.verticalcontainer = Div ().ac ('bigboardverticalcontainer');
				self.movelistdivwidth = 100;
				self.movelistdiv = Div ().ac ('bigboardmovelist').w (self.movelistdivwidth).mw (self.movelistdivwidth);
				self.analysisdiv = Div ();
				self.analysiscontrolpaneltop = Div ().ac ('bigboardanalysiscontrolpanel');
				self.analysiscontrolpaneltop.a (Button ('#', self.gamehere).ac ('analysiscontrol'));
				self.analysiscontrolpaneltop.a (Button ('<<', self.gametobegin).ac ('analysiscontrol'));
				self.analysiscontrolpaneltop.a (Button ('<', self.gameback).ac ('analysiscontrol').w (60));
				self.analysiscontrolpaneltop.a (Button ('>', self.gameforward).ac ('analysiscontrol').w (60));
				self.analysiscontrolpaneltop.a (Button ('>>', self.gametoend).ac ('analysiscontrol'));
				self.analysiscontrolpaneltop.a (Button ('Store >', self.storeforward).ac ('analysismake'));
				self.analysiscontrolpaneltop.a (Button ('Store Make', self.storemake).ac ('analysismake'));
				self.analysiscontrolpaneltop.a (Button ('Store Stop', self.stopandstoreanalysis).ac ('analysisstop'));
				self.analysiscontrolpanelbottom = Div ().ac ('bigboardanalysiscontrolpanel');
				self.analysiscontrolpanelbottom.a (Button ('#', self.getstoredanalysisinfo).ac ('analysisanalyze'));
				self.analysiscontrolpanelbottom.a (Button ('Analyze', self.analyzecallbackfactory ()).ac ('analysisanalyze'));
				self.analysiscontrolpanelbottom.a (Button ('Analyze all', self.analyzecallbackfactory (true)).ac ('analysisanalyze'));
				self.analysiscontrolpanelbottom.a (Button ('Quick all', self.analyzecallbackfactory (true, 5, null)).ac ('analysisanalyze'));
				self.analysiscontrolpanelbottom.a (Button ('Make', self.makeanalyzedmovecallback).ac ('analysismake'));
				self.analysiscontrolpanelbottom.a (Button ('Stop', self.stopanalyzecallback).ac ('analysisstop'));
				self.analysiscontrolpanelbottom.a (Button ('Store', self.storeanalysiscallback).ac ('analysisstore'));
				var mopts = dict ({});
				for (var i = 1; i < 21; i++) {
					mopts [str (i)] = 'MultiPV {}'.format (i);
				}
				self.multipvcombo = ComboBox (dict ({'selectclass': 'boardmultipvcomboselect', 'optionfirstclass': 'boardmultipvcombooptionfirst', 'optionclass': 'boardmultipvcombooption'})).setoptions (mopts, str (self.defaultmultipv));
				self.analysiscontrolpanelbottom.a (self.multipvcombo);
				self.analysisdiv.aa (list ([self.analysiscontrolpaneltop, self.analysiscontrolpanelbottom]));
				self.analysisinfodiv = Div ();
				self.analysisdiv.a (self.analysisinfodiv);
				self.gamesdiv = Div ();
				self.gamediv = Div ();
				self.pgntext = PgnText ();
				self.tabpane = TabPane (dict ({'kind': 'normal', 'id': 'board'})).setTabs (list ([Tab ('analysis', 'Analysis', self.analysisdiv), Tab ('game', 'Game', self.gamediv), Tab ('pgn', 'Pgn', self.pgntext), Tab ('games', 'Games', self.gamesdiv)]), 'analysis');
				self.verticalcontainer.aa (list ([self.sectioncontainer, self.movelistdiv, self.tabpane]));
				self.a (self.verticalcontainer);
				self.basicresize ();
				self.buildpositioninfo ();
				self.sioreq (dict ({'kind': 'retrievedb', 'owner': 'board', 'path': 'board/variantkey'}));
			});}
		});
		if (window.location.protocol == 'https:') {
			var ws_scheme = 'wss://';
		}
		else {
			var ws_scheme = 'ws://';
		}
		var SUBMIT_URL = ws_scheme + window.location.host;
		var queryparamsstring = window.location.search;
		var queryparams = dict ({});
		if (len (queryparamsstring) > 1) {
			var queryparamsstring = queryparamsstring.__getslice__ (1, null, 1);
			var mainparts = queryparamsstring.py_split ('&');
			var __iterable0__ = mainparts;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var mainpart = __iterable0__ [__index0__];
				var parts = mainpart.py_split ('=');
				queryparams [parts [0]] = parts [1];
			}
		}
		var ENGINE_CMD_ALIASES = dict ({'start': dict ({'display': 'R', 'cmds': list (['r'])}), 'stop': dict ({'display': 'S', 'cmds': list (['s'])}), 'parseuci': dict ({'display': 'Parse UCI options', 'cmds': list (['r', 'parseuci'])}), 'd15': dict ({'display': 'd15', 'cmds': list (['go depth 15'])})});
		var BOT_CMD_ALIASES = dict ({'start': dict ({'display': 'R', 'cmds': list (['r'])}), 'stop': dict ({'display': 'S', 'cmds': list (['s'])}), 'loadconfig': dict ({'display': 'LC', 'cmds': list (['s', 'r'])})});
		var CBUILD_CMD_ALIASES = dict ({'stop': dict ({'display': 'S', 'cmds': list (['s'])}), 'example': dict ({'display': 'example build', 'cmds': list (['-e antichess --variant antichess --nextlichessdb -a'])}), 'help': dict ({'display': 'help', 'cmds': list (['-h'])})});
		var socket = null;
		var processconsoles = dict ({'engine': null, 'bot': null, 'cbuild': null});
		var mainlogpane = null;
		var maintabpane = null;
		var mainboard = null;
		var configschema = SchemaDict (dict ({}));
		var srcdiv = Div ().ms ().fs (20);
		var schemajson = null;
		var getlocalconfig = function () {
			socket.emit ('sioreq', dict ({'kind': 'getlocalconfig'}));
		};
		var showsrc = function () {
			var srcjsoncontent = JSON.stringify (serializeconfig (), null, 2);
			srcdiv.html (('<pre>' + srcjsoncontent) + '</pre>');
			maintabpane.selectByKey ('src');
		};
		var serializeconfig = function () {
			var obj = dict ({'config': configschema.topureobj (), 'configschema': configschema.toobj ()});
			return obj;
		};
		var deserializeconfig = function (obj) {
			var schemaobj = dict ({});
			try {
				if (__in__ ('configschema', obj)) {
					var schemaobj = obj ['configschema'];
				}
				configschema = schemafromobj (schemaobj);
			}
			catch (__except0__) {
				print ('deserialize config obj failed for', obj);
			}
		};
		var deserializeconfigcontent = function (content) {
			try {
				var obj = JSON.parse (content);
				deserializeconfig (obj);
			}
			catch (__except0__) {
				print ('deserializing config content failed for', content);
			}
			maintabpane.setTabElementByKey ('config', buildconfigdiv ());
		};
		var buildconfigdiv = function () {
			var configsplitpane = SplitPane (dict ({'controlheight': 50}));
			configsplitpane.controldiv.aa (list ([Button ('Serialize', serializecallback).fs (24), Button ('Reload', reloadcallback).fs (16), Button ('Show source', showsrc).fs (16)])).bc ('#ddd');
			var configschemacontainerdiv = Div ().ac ('configschemacontainerdiv').a (configschema);
			configsplitpane.setcontent (configschemacontainerdiv);
			return configsplitpane;
		};
		var getbincallback = function (content) {
			deserializeconfigcontent (content);
		};
		var getbinerrcallback = function (err) {
			print ('get bin failed with', err);
		};
		var mainlog = function (logitem) {
			mainlogpane.log.log (logitem);
		};
		var log = function (content, dest) {
			if (typeof dest == 'undefined' || (dest != null && dest .hasOwnProperty ("__kwargtrans__"))) {;
				var dest = 'engine';
			};
			var li = LogItem (('<pre>' + content) + '</pre>');
			processconsoles [dest].log.log (li);
		};
		var cmdinpcallback = function (cmd, key) {
			socket.emit ('sioreq', dict ({'kind': 'cmd', 'key': key, 'data': cmd}));
		};
		var serializeputjsonbincallback = function (content) {
			try {
				var obj = JSON.parse (content);
				var binid = 'local';
				if (__in__ ('id', obj)) {
					var binid = obj ['id'];
				}
				else if (__in__ ('parentId', obj)) {
					var binid = obj ['parentId'];
				}
				if (!(binid == 'local')) {
					socket.emit ('sioreq', dict ({'kind': 'storebinid', 'data': binid}));
				}
				var href = (((window.location.protocol + '//') + window.location.host) + '/?id=') + binid;
				document.location.href = href;
			}
			catch (__except0__) {
				print ('there was an error parsing json', content);
				return ;
			}
			return null;
		};
		var serializeputjsonbinerrcallback = function (err) {
			print ('there was an error putting to json bin', err);
		};
		var serializecallback = function () {
			var json = JSON.stringify (serializeconfig (), null, 2);
			socket.emit ('sioreq', dict ({'kind': 'storeconfig', 'data': json}));
		};
		var reloadcallback = function () {
			document.location.href = '/';
		};
		var mainboardmovecallback = function (variantkey, fen, moveuci) {
			setTimeout ((function __lambda__ (ev) {
				return socket.emit ('sioreq', dict ({'kind': 'mainboardmove', 'variantkey': variantkey, 'fen': fen, 'moveuci': moveuci}));
			}), simulateserverlag ());
		};
		var mainboardvariantchangedcallback = function (variantkey) {
			setTimeout ((function __lambda__ (ev) {
				return socket.emit ('sioreq', dict ({'kind': 'mainboardsetvariant', 'variantkey': variantkey}));
			}), simulateserverlag ());
		};
		var mainboardmoveclickedcallback = function (variantkey, fen, moveuci) {
			setTimeout ((function __lambda__ (ev) {
				return socket.emit ('sioreq', dict ({'kind': 'mainboardmove', 'variantkey': variantkey, 'fen': fen, 'moveuci': moveuci}));
			}), simulateserverlag ());
		};
		var mainboardenginecommandcallback = function (sline) {
			socket.emit ('sioreq', dict ({'kind': 'cmd', 'key': 'engine', 'data': sline}));
		};
		var build = function () {
			processconsoles ['engine'] = ProcessConsole (dict ({'key': 'engine', 'cmdinpcallback': cmdinpcallback, 'cmdaliases': ENGINE_CMD_ALIASES}));
			processconsoles ['bot'] = ProcessConsole (dict ({'key': 'bot', 'cmdinpcallback': cmdinpcallback, 'cmdaliases': BOT_CMD_ALIASES}));
			processconsoles ['cbuild'] = ProcessConsole (dict ({'key': 'cbuild', 'cmdinpcallback': cmdinpcallback, 'cmdaliases': CBUILD_CMD_ALIASES}));
			mainlogpane = LogPane ();
			mainboard = Board (dict ({'movecallback': mainboardmovecallback, 'variantchangedcallback': mainboardvariantchangedcallback, 'moveclickedcallback': mainboardmoveclickedcallback, 'enginecommandcallback': mainboardenginecommandcallback, 'socket': socket}));
			maintabpane = TabPane (dict ({'kind': 'main', 'id': 'main'})).setTabs (list ([Tab ('engineconsole', 'Engine console', processconsoles ['engine']), Tab ('botconsole', 'Bot console', processconsoles ['bot']), Tab ('cbuildconsole', 'Cbuild console', processconsoles ['cbuild']), Tab ('upload', 'Upload', FileUploader (dict ({'url': '/upload'}))), Tab ('dirbrowser', 'Dirbrowser', DirBrowser ()), Tab ('board', 'Board', mainboard), Tab ('config', 'Config', buildconfigdiv ()), Tab ('log', 'Log', mainlogpane), Tab ('src', 'Src', srcdiv), Tab ('about', 'About', Div ().ac ('appabout').html ('Lichess GUI bot.'))]), 'botconsole');
			ge ('maintabdiv').innerHTML = '';
			ge ('maintabdiv').appendChild (maintabpane.e);
		};
		var onconnect = function () {
			mainlog (LogItem ('socket connected ok', 'cmdstatusok'));
			socket.emit ('sioreq', dict ({'data': 'socket connected'}));
			getlocalconfig ();
			socket.emit ('sioreq', dict ({'kind': 'mainboardsetvariant', 'variantkey': 'standard'}));
		};
		var onevent = function (json) {
			var dest = null;
			var logitem = null;
			if (__in__ ('kind', json)) {
				var kind = json ['kind'];
				if (kind == 'procreadline') {
					var dest = json ['prockey'];
					var sline = json ['sline'];
					var logitem = LogItem (sline, 'cmdreadline');
					if (dest == 'bot') {
						if (len (sline) > 0) {
							if (sline [0] == '!') {
								var logitem = LogItem ('bot error:' + sline.__getslice__ (1, null, 1), 'cmdstatuserr');
							}
						}
					}
				}
				else if (kind == 'ucioptionsparsed') {
					var ucioptionsobj = json ['ucioptions'];
					var ucischema = schemafromucioptionsobj (ucioptionsobj);
					var selfprofile = getpathfromschema (configschema, 'profile/#');
					if (selfprofile === null) {
						window.alert ('Warning: no profile selected to store UCI options.');
					}
					else {
						selfprofile.setchildatkey ('ucioptions', ucischema);
						maintabpane.setTabElementByKey ('config', buildconfigdiv ());
						maintabpane.selectByKey ('config');
						window.alert ('UCI options stored in current profile.');
					}
				}
				else if (kind == 'analysisinfo') {
					mainboard.processanalysisinfo (json ['analysisinfo']);
				}
			}
			if (__in__ ('response', json)) {
				var status = '?';
				var response = json ['response'];
				if (__in__ ('key', response)) {
					var dest = response ['key'];
				}
				else if (kind == 'check') {
					item.value = 'false';
					if (py_default) {
						item.value = 'true';
					}
					item.writepreference.check = true;
					item.setenabled (py_default);
					item.build ();
				}
				if (__in__ ('kind', response)) {
					var kind = response ['kind'];
					if (kind == 'setlocalconfig') {
						var data = response ['data'];
						deserializeconfigcontent (data);
						mainboard.setconfigschema (configschema);
					}
					else if (kind == 'configstored') {
						window.alert (('Config storing status: ' + status) + '.');
						mainboard.setconfigschema (configschema);
					}
					else if (kind == 'setmainboardfen') {
						var fen = response ['fen'];
						var positioninfo = response ['positioninfo'];
						mainboard.setfromfen (fen, positioninfo);
					}
				}
				if (__in__ ('owner', response)) {
					var owner = response ['owner'];
					if (owner == 'board') {
						mainboard.siores (response);
					}
				}
				if (__in__ ('owner', response)) {
					var owner = response ['owner'];
					if (owner == 'board') {
						mainboard.siores (response);
					}
					item.openchilds ();
					item.openchilds ();
				}
				item.setchildparent (ucioptions);
				var nameditem = NamedSchemaItem (dict ({'key': key, 'item': item}));
				ucioptions.childs.append (nameditem);
			}
			if (logitem === null || dest === null) {
				var jsonstr = JSON.stringify (json, null, 2);
				mainlog (LogItem (jsonstr));
			}
			else {
				processconsoles [dest].log.log (logitem);
			}
		};
		var windowresizehandler = function () {
			maintabpane.resize ();
		};
		console.log ('creating socket for submit url [ {} ]'.format (SUBMIT_URL));
		var socket = io.connect (SUBMIT_URL);
		console.log ('socket created ok');
		build ();
		socket.on ('connect', onconnect);
		socket.on ('siores', (function __lambda__ (json) {
			return onevent (json);
		}));
		addEventListener (window, 'resize', windowresizehandler);
		__pragma__ ('<all>')
			__all__.ANTICHESS_START_FEN = ANTICHESS_START_FEN;
			__all__.BLACK = BLACK;
			__all__.BOT_CMD_ALIASES = BOT_CMD_ALIASES;
			__all__.BasicBoard = BasicBoard;
			__all__.Board = Board;
			__all__.Button = Button;
			__all__.CBUILD_CMD_ALIASES = CBUILD_CMD_ALIASES;
			__all__.CRAZYHOUSE_START_FEN = CRAZYHOUSE_START_FEN;
			__all__.Canvas = Canvas;
			__all__.CheckBox = CheckBox;
			__all__.ComboBox = ComboBox;
			__all__.ComboOption = ComboOption;
			__all__.DEFAULT_ENABLED = DEFAULT_ENABLED;
			__all__.DEFAULT_HELP = DEFAULT_HELP;
			__all__.DOUBLE_EXCLAM_LIMIT = DOUBLE_EXCLAM_LIMIT;
			__all__.DRAWISH_LIMIT = DRAWISH_LIMIT;
			__all__.DirBrowser = DirBrowser;
			__all__.Div = Div;
			__all__.ENGINE_CMD_ALIASES = ENGINE_CMD_ALIASES;
			__all__.EXCLAM_LIMIT = EXCLAM_LIMIT;
			__all__.FileInput = FileInput;
			__all__.FileUploader = FileUploader;
			__all__.Form = Form;
			__all__.HORDE_START_FEN = HORDE_START_FEN;
			__all__.INTERESTING_LIMIT = INTERESTING_LIMIT;
			__all__.Input = Input;
			__all__.LICH_API_GAMES_EXPORT = LICH_API_GAMES_EXPORT;
			__all__.Label = Label;
			__all__.LabeledLinkedCheckBox = LabeledLinkedCheckBox;
			__all__.LinkedCheckBox = LinkedCheckBox;
			__all__.LinkedSlider = LinkedSlider;
			__all__.LinkedTextInput = LinkedTextInput;
			__all__.LinkedTextarea = LinkedTextarea;
			__all__.Log = Log;
			__all__.LogItem = LogItem;
			__all__.LogPane = LogPane;
			__all__.MATE_LIMIT = MATE_LIMIT;
			__all__.MATE_SCORE = MATE_SCORE;
			__all__.MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH;
			__all__.MAX_LINE_LENGTH = MAX_LINE_LENGTH;
			__all__.Move = Move;
			__all__.MultipvInfo = MultipvInfo;
			__all__.NamedSchemaItem = NamedSchemaItem;
			__all__.Option = Option;
			__all__.P = P;
			__all__.PIECE_KINDS = PIECE_KINDS;
			__all__.PIECE_NAMES = PIECE_NAMES;
			__all__.PROMISING_LIMIT = PROMISING_LIMIT;
			__all__.PROMPIECEKINDS_ANTICHESS = PROMPIECEKINDS_ANTICHESS;
			__all__.PROMPIECEKINDS_STANDARD = PROMPIECEKINDS_STANDARD;
			__all__.PgnInfo = PgnInfo;
			__all__.PgnList = PgnList;
			__all__.PgnText = PgnText;
			__all__.Piece = Piece;
			__all__.PieceStore = PieceStore;
			__all__.ProcessConsole = ProcessConsole;
			__all__.RACING_KINGS_START_FEN = RACING_KINGS_START_FEN;
			__all__.RawTextInput = RawTextInput;
			__all__.SCHEMA_WRITE_PREFERENCE_DEFAULTS = SCHEMA_WRITE_PREFERENCE_DEFAULTS;
			__all__.SCROLL_BAR_WIDTH = SCROLL_BAR_WIDTH;
			__all__.STANDARD_START_FEN = STANDARD_START_FEN;
			__all__.SUBMIT_URL = SUBMIT_URL;
			__all__.SchemaCollection = SchemaCollection;
			__all__.SchemaDict = SchemaDict;
			__all__.SchemaItem = SchemaItem;
			__all__.SchemaList = SchemaList;
			__all__.SchemaScalar = SchemaScalar;
			__all__.SchemaWritePreference = SchemaWritePreference;
			__all__.Select = Select;
			__all__.Slider = Slider;
			__all__.Span = Span;
			__all__.SplitPane = SplitPane;
			__all__.Square = Square;
			__all__.THREE_CHECK_START_FEN = THREE_CHECK_START_FEN;
			__all__.Tab = Tab;
			__all__.TabPane = TabPane;
			__all__.TextArea = TextArea;
			__all__.TextInputWithButton = TextInputWithButton;
			__all__.VARIANT_OPTIONS = VARIANT_OPTIONS;
			__all__.Vect = Vect;
			__all__.View = View;
			__all__.WHITE = WHITE;
			__all__.WINDOW_SAFETY_MARGIN = WINDOW_SAFETY_MARGIN;
			__all__.WINNING_MOVE_LIMIT = WINNING_MOVE_LIMIT;
			__all__.__name__ = __name__;
			__all__.addEventListener = addEventListener;
			__all__.build = build;
			__all__.buildconfigdiv = buildconfigdiv;
			__all__.ce = ce;
			__all__.choose = choose;
			__all__.cmdinpcallback = cmdinpcallback;
			__all__.configschema = configschema;
			__all__.cpick = cpick;
			__all__.deserializeconfig = deserializeconfig;
			__all__.deserializeconfigcontent = deserializeconfigcontent;
			__all__.e = e;
			__all__.ge = ge;
			__all__.getClientVect = getClientVect;
			__all__.getScrollBarWidth = getScrollBarWidth;
			__all__.getbincallback = getbincallback;
			__all__.getbinerrcallback = getbinerrcallback;
			__all__.getclassforpiece = getclassforpiece;
			__all__.getfromobj = getfromobj;
			__all__.getglobalcssvar = getglobalcssvar;
			__all__.getglobalcssvarpxint = getglobalcssvarpxint;
			__all__.getjson = getjson;
			__all__.getjsonbin = getjsonbin;
			__all__.getlocalconfig = getlocalconfig;
			__all__.getpathfromschema = getpathfromschema;
			__all__.getpathlistfromschema = getpathlistfromschema;
			__all__.getscalarfromschema = getscalarfromschema;
			__all__.getstartfenforvariantkey = getstartfenforvariantkey;
			__all__.isvalidpieceletter = isvalidpieceletter;
			__all__.lichapiget = lichapiget;
			__all__.log = log;
			__all__.mainboard = mainboard;
			__all__.mainboardenginecommandcallback = mainboardenginecommandcallback;
			__all__.mainboardmovecallback = mainboardmovecallback;
			__all__.mainboardmoveclickedcallback = mainboardmoveclickedcallback;
			__all__.mainboardvariantchangedcallback = mainboardvariantchangedcallback;
			__all__.mainlog = mainlog;
			__all__.mainlogpane = mainlogpane;
			__all__.mainpart = mainpart;
			__all__.mainparts = mainparts;
			__all__.maintabpane = maintabpane;
			__all__.onconnect = onconnect;
			__all__.onevent = onevent;
			__all__.parsejson = parsejson;
			__all__.parts = parts;
			__all__.patchclasses = patchclasses;
			__all__.piececolortocolorname = piececolortocolorname;
			__all__.piecekindtopiecename = piecekindtopiecename;
			__all__.piecelettertopiece = piecelettertopiece;
			__all__.processconsoles = processconsoles;
			__all__.prompiecekindsforvariantkey = prompiecekindsforvariantkey;
			__all__.putjsonbin = putjsonbin;
			__all__.queryparams = queryparams;
			__all__.queryparamsstring = queryparamsstring;
			__all__.randint = randint;
			__all__.randscalarvalue = randscalarvalue;
			__all__.reloadcallback = reloadcallback;
			__all__.schemaclipboard = schemaclipboard;
			__all__.schemafromobj = schemafromobj;
			__all__.schemafromucioptionsobj = schemafromucioptionsobj;
			__all__.schemajson = schemajson;
			__all__.schemawritepreferencefromobj = schemawritepreferencefromobj;
			__all__.scorecolor = scorecolor;
			__all__.scoreverbal = scoreverbal;
			__all__.serializecallback = serializecallback;
			__all__.serializeconfig = serializeconfig;
			__all__.serializeputjsonbincallback = serializeputjsonbincallback;
			__all__.serializeputjsonbinerrcallback = serializeputjsonbinerrcallback;
			__all__.showsrc = showsrc;
			__all__.simulateserverlag = simulateserverlag;
			__all__.socket = socket;
			__all__.srcdiv = srcdiv;
			__all__.striplonglines = striplonglines;
			__all__.uci_variant_to_variantkey = uci_variant_to_variantkey;
			__all__.uid = uid;
			__all__.windowresizehandler = windowresizehandler;
			__all__.ws_scheme = ws_scheme;
			__all__.xor = xor;
		__pragma__ ('</all>')
	}) ();
    return __all__;
}
window ['app'] = app ();
